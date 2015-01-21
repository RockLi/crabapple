# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from flask import render_template, redirect


class ControllerSpec(object):

    def __init__(self, server):
        self.server = server

    def view_specs(self):
        return render_template('specs.html', specs=self.server.store.get_all_specs())

    def view_spec_disable(self, spec_id):
        s = self.server.store.get_spec(spec_id)
        if s:
            s.enabled = not s.enabled
        return redirect('/specs')

    def view_spec_detail(self, spec_id):
        s = self.server.store.get_spec(spec_id)
        print s
        if s is None:
            return redirect('/specs')
        return render_template('spec.html', spec=s)

    def register(self, app):
        app.add_url_rule('/specs', 'view_specs', self.view_specs)
        app.add_url_rule('/spec/<int:spec_id>/enable', 'view_spec_disable', self.view_spec_disable)
        app.add_url_rule('/spec/<int:spec_id>', 'view_spec_detail', self.view_spec_detail)
