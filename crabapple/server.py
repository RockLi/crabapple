# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import sys
import os
import threading
import Queue
import logging
import datetime
import subprocess
from flask import Flask, redirect
from flask import request, make_response

from crabapple.spec import Spec
from crabapple.util import get_logger
from crabapple.objects import (
    Deployment,
    Commit,
    DeploymentStatus,
)
from crabapple.store.store import Store


class Server(object):

    def __init__(self, logger=None, config=None):
        self.logger = logger if logger else get_logger()
        self.event_handlers = {
            'push': self.push_handler
        }
        self.app = Flask(__name__)
        self.config = config
        self.logdir = config.logdir
        self.datadir = config.datadir
        if self.config.logdir is not None and \
          not os.path.exists(self.config.logdir):
            os.makedirs(self.config.logdir)
        if self.config.datadir is not None and \
          not os.path.exists(self.config.datadir):
            os.makedirs(self.config.datadir)

        if self.config.store == 'memory':
            self.store = Store('memory', self.config.datadir)
        elif self.config.store == 'sqlite':
            self.store = Store('sqlite', self.config.datadir)
        elif self.config.store == 'mysql':
            self.store = Store('mysql',
                                self.config.datadir,
                                **self.config.store_mysql)
        elif self.config.store == 'postgresql':
            self.store = Store('postgresql',
                                self.config.datadir,
                                **self.config.store_postgresql)
        else:
            self.logger.critical('Unknown persistent method')
            sys.exit(1)

        self.store.setup()

        if self.config.specs is not None:
            for spec_file in self.config.specs:
                spec = Spec.parse_file(spec_file)
                if spec is None:
                    self.logger.critical('Spec file is not written correctly')
                    sys.exit(1)
                self.store.insert_spec(spec)

        self.deployments = Queue.Queue()
        t = threading.Thread(target=self.do_deployment)
        t.daemon = True
        t.start()

    def trigger_deployment(self, deployment):
        self.store.insert_deployment(deployment)
        self.deployments.put(deployment)

    def do_deployment(self):
        while True:
            deployment_object = self.deployments.get()
            spec = self.store.get_spec(deployment_object.spec_id)
            deployment_object.start_time = datetime.datetime.now()
            self.logger.info('Begin to do the deployment[#%s], triggered_by: %s, triggered commit: %s.',
                             deployment_object.id,
                             deployment_object.pusher_name,
                             deployment_object.triggered_commit.id)
            deployment_object.mark_status(DeploymentStatus.STARTED)
            self.store.update_deployment(deployment_object)
            try:
                result = subprocess.check_output("crabapple deploy --spec %s" % (spec.path,), shell=True)
                deployment_object.mark_status(DeploymentStatus.SUCCESS)
            except subprocess.CalledProcessError:
                deployment_object.mark_status(DeploymentStatus.FAILED)
            finally:
                deployment_object.end_time = datetime.datetime.now()
            self.store.update_deployment(deployment_object)
            self.deployments.task_done()

            result = '''Deployment started at: {0}

Triggered By {1}<{2}>,

triggered commit: {3}.

+++++ OUTPUT ++++++


'''.format(deployment_object.start_time.strftime('%Y-%m-%d %H:%M:%S'),
           deployment_object.pusher_name,
           deployment_object.pusher_email,
           deployment_object.triggered_commit.id) + result + '''

+++++ END ++++++

Deployment ended at: {0}, Status: {1}!
            '''.format(deployment_object.end_time.strftime('%Y-%m-%d %H:%M:%S'),
                       'Success' if deployment_object.status == DeploymentStatus.SUCCESS else 'Failed')

            print '-' * 20
            print result
            print '+' * 20

            with open(self.logdir + '/' + str(deployment_object.id) + '.log', 'w') as f:
                f.write(result)

            self.logger.info('Deployment[#%s] done, status: %s.',
                             deployment_object.id,
                             'Success' if deployment_object.status == DeploymentStatus.SUCCESS else 'Failed')

            if not spec.notifiers:
                continue

            for notifier in spec.notifiers:
                if notifier.name == 'email':
                    notifier.send(msg=result,
                                  subject='Deployment #{0}, {1} at {2}'.format(deployment_object.id,
                                                                               'Successful' if deployment_object.is_successful() else 'Failed',
                                                                               datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))


    def push_handler(self, payload):
        repo_name = payload.get('repository', {}).get('name', None)
        if repo_name is None:
            return

        spec = self.store.get_spec_by_name(repo_name)
        if spec is None or not spec.enabled:
            return

        deployment_object = Deployment.parse_from_github(payload,
                                                         self.store)
        if not spec.is_watched_branch(deployment_object.branch):
            return

        deployment_object.spec_id = spec.id
        self.trigger_deployment(deployment_object)

    def __daemon(self):
        pid = os.fork()
        # @FixMe: dup and close fds
        if pid == 0:
            os.setsid()
        else:
            os._exit(0)

    def start(self):
        if self.config.daemon:
            self.__daemon()

        self.__start()

    def __start_admin(self):
        @self.app.route('/', methods=['GET'])
        def index():
            return redirect('/deployments')

        from crabapple.admin.controller.deployment import ControllerDeployment
        from crabapple.admin.controller.spec import ControllerSpec
        for cls in [ControllerDeployment, ControllerSpec]:
            c = cls(self)
            c.register(self.app)

    def __start(self):
        @self.app.route('/github/event_handler', methods=['POST'])
        def github_event_handler():
            github_event = request.headers.get('X-Github-Event', None)
            github_signature = request.headers.get('X-Hub-Signature', None)
            github_delivery = request.headers.get('X-Github-Delivery', None)
            if github_event is None or github_signature is None or github_delivery is None:
                return make_response('unexpected request source', 400)

            handler = self.event_handlers.get(github_event, None)
            if handler is None:
                return ''

            try:
                payload = request.get_json()
            except Exception:
                response = make_response('unexpected data', 400)
                return response
            try:
                handler(payload)
            except Exception, e:
                return make_response('unexpected data', 400)

            return ''

        if self.config.admin:
            self.__start_admin()

        logger = logging.getLogger('werkzeug')
        for handler in self.logger.handlers:
            self.app.logger.addHandler(handler)
            logger.addHandler(handler)
        self.app.logger.setLevel(logging.INFO)
        self.logger.info('crabapple.server started')
        if self.config.admin:
            self.logger.info('crabapple.server admin UI enabled')
        self.app.run(host=self.config.host, port=self.config.port)
