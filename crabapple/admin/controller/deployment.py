# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import datetime
from flask import render_template, redirect, request
from crabapple.objects import Commit, Deployment, DeploymentStatus


class ControllerDeployment(object):

    def __init__(self, server):
        self.server = server

    def view_deployments(self):
        return render_template('index.html',
                               deployments=self.server.store.get_all_deployments(),
                               specs={o.id: o for o in self.server.store.get_all_specs()})

    def view_deployment(self, deployment_id):
        deployment_object = self.server.store.get_deployment(deployment_id)
        if deployment_object is None:
            return redirect('/')

        content = ''
        try:
            with open(self.server.config.logdir + '/' + str(deployment_object.id) + '.log') as f:
                content = f.read()
        except IOError:
            content = ''

        return render_template('deployment_view.html', deployment=deployment_object, content=content)

    def view_deploy(self):
        if request.method == 'GET':
            return render_template('deploy.html', specs=self.server.store.get_all_specs())
        elif request.method == 'POST':
            spec = request.form['spec']
            commit = request.form['commit']

            c = Commit()
            c.hash = commit

            o = Deployment(status=DeploymentStatus.SCHEDULED,
                           triggered_time=datetime.datetime.now())
            o.spec_id = int(spec)
            o.branch = '* Manual *'
            o.triggered_commit = c
            o.pusher_name = 'admin'
            o.pusher_email = '-'
            self.server.trigger_deployment(o)
            return redirect('/deployments')

    def register(self, app):
        app.add_url_rule('/deployments', 'view_deployments', self.view_deployments)
        app.add_url_rule('/deploy', 'view_deploy', self.view_deploy, methods=['GET', 'POST'])
        app.add_url_rule('/deployment/<int:deployment_id>', 'view_deployment', self.view_deployment)
