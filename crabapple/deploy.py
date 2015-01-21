# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import sys
import os
import inspect
from crabapple.spec import Spec


class Deployer(object):

    def __init__(self, spec_file):
        self.spec = Spec.parse_file(spec_file)
        if self.spec is None:
            print 'Failed to do the deployment due to the invalid spec'
            sys.exit(1)

        os.chdir(self.spec.root)

    def report_result(self, success):
        if success:
            print 'Deployed successfully.'
        else:
            print 'Deployed failed.'

    def do(self):
        success = False
        print 'Ready to deploy for %s...' % (self.spec.name,)
        if self.spec.on_test:
            if inspect.isfunction(self.spec.on_test):
                print 'Begin to run the testing...'
                success = self.spec.on_test()
            else:
                print 'on_test must be a function in your spec file'
                self.report_result(False)
                return
        else:
            success = True

        if success is not None and not success:
            print 'Testing failed, abort now.'
            self.report_result(success)
            return

        if self.spec.on_deploy:
            if inspect.isfunction(self.spec.on_deploy):
                print 'Begin to do the deployment...'
                success = self.spec.on_deploy()
            else:
                print 'on_deploy must be a function in your spec file'
                self.report_result(False)
                return
        else:
            success = True

        if success is not None and not success:
            print 'Deployment failed, abort now.'
        else:
            success = True
        self.report_result(success)
