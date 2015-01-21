# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import imp

from crabapple.util import get_logger
from crabapple.notifier.email_notifier import EmailNotifier


logger = get_logger()


class Spec(object):

    attributes = {
        'syntax_version': 1.0,

        'name': None,
        'repo_url': None,

        'watched_branches': None,

        'notifiers': None,
        'notifier_email': None,

        'deploy_timeout': 0,
        'on_deploy': None,
        'test_timeout': 0,
        'on_test': None,
    }

    def __init__(self, filename=None):
        self.id = None
        self.path = os.path.abspath(filename)
        self.root = os.path.dirname(self.path)
        self.enabled = True

    def __getattr__(self, name):
        return self.attributes.get(name)

    def __setattr__(self, name, value):
        self.attributes[name] = value

    def is_watched_branch(self, branch):
        if isinstance(self.watched_branches, list):
            return branch in self.watched_branches or '*' in self.watched_branches
        else:
            return branch == self.watched_branches or self.watched_branches == '*'

    @staticmethod
    def parse_file(filename):
        if not os.path.exists(filename):
            logger.critical('Spec file: %s not found', (filename))
            return None

        try:
            m = imp.load_source('m', filename)
        except Exception, e:
            logger.critical('Failed to parse your spec file: %s, %s', (filename, e))
            return None

        s = Spec(filename)
        for attr in Spec.attributes.keys():
            if getattr(m, attr, None):
                setattr(s, attr, getattr(m, attr))

        if s.watched_branches is None:
            s.watched_branches = ['master']

        if s.notifiers:
            for idx, notifier in enumerate(s.notifiers):
                if notifier == 'email':
                    notifier = EmailNotifier()
                    notifier.config(s.notifier_email)
                    s.notifiers[idx] = notifier

        return s
