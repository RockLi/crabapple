# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import imp


class ServerConfig(object):

    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 50000
        self.daemon = False
        self.logdir = './log'
        self.datadir = './data'
        self.admin = False
        self.specs = []
        self.store = 'memory'
        self.store_mysql = {
            'username': 'crabapple',
            'password': 'crabapple',
            'hostname': '127.0.0.1',
            'port': 3306,
            'db': 'crabapple',
        }
        self.store_postgresql = {
            'username': 'crabapple',
            'password': 'crabapple',
            'hostname': '127.0.0.1',
            'port': 5432,
            'db': 'crabapple',
        }

    @staticmethod
    def load_from_file(filename):
        try:
            c = imp.load_source('c', filename)
        except Exception:
            return None

        sc = ServerConfig()
        if hasattr(c, 'host'):
            sc.host = c.host
        if hasattr(c, 'port'):
            sc.port = c.port
        if hasattr(c, 'daemon'):
            sc.daemon = c.daemon
        if hasattr(c, 'logdir'):
            sc.logdir = c.logdir
        if hasattr(c, 'datadir'):
            sc.datadir = c.datadir
        if hasattr(c, 'admin'):
            sc.admin = c.admin
        if hasattr(c, 'specs'):
            sc.specs = c.specs
        if hasattr(c, 'store'):
            sc.store = c.lower()

        if hasattr(c, 'mysql_username'):
            sc.store_mysql['username'] = c.mysql_username
        if hasattr(c, 'mysql_password'):
            sc.store_mysql['password'] = c.mysql_password
        if hasattr(c, 'mysql_hostname'):
            sc.store_mysql['hostname'] = c.mysql_hostname
        if hasattr(c, 'mysql_port'):
            sc.store_mysql['port'] = int(c.mysql_port)
        if hasattr(c, 'mysql_db'):
            sc.store_mysql['db'] = c.mysql_db

        if hasattr(c, 'postgresql_username'):
            sc.store_postgresql['username'] = c.postgresql_username
        if hasattr(c, 'postgresql_password'):
            sc.store_postgresql['password'] = c.postgresql_password
        if hasattr(c, 'postgresql_hostname'):
            sc.store_postgresql['hostname'] = c.postgresql_hostname
        if hasattr(c, 'postgresql_port'):
            sc.store_postgresql['port'] = int(c.postgresql_port)
        if hasattr(c, 'postgresql_db'):
            sc.store_postgresql['db'] = c.postgresql_db

        return sc
