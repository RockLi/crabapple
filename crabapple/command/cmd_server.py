# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import os
import sys
import imp
import getopt
import logging

from crabapple.server import Server
from crabapple.exception import InvalidArgsException
from crabapple.util import get_logger
from crabapple.config import ServerConfig


help_msg = '''Use crabapple server to create a HTTP server listening events from Github.

crabapple server [--config config_file] [--host 127.0.0.1] [--port 50000] [--daemon] [--spec xx] [--admin] [--logdir ./log] [--datadir ./data]

config:
    load the options from the configuration file

host:
    which host to listen, default to '127.0.0.1'

port:
    which port to bind, default to '50000'

daemon:
    create a daemon process

spec:
    spec file to use when doing the deployment

logdir:
    directory to put all your logs

datadir:
    directory to store all persistent data

admin:
    enable the admin management UI

store:
    which kind of persistent store to use, default to sqlite
    memory:     dismiss after each crabapple server restart
    sqlite:     store data in sqlite3
    mysql:      store data in mysql
    postgresql: store data in PostgreSQL
    file:       store data in one file

mysql-username:
    default to crabapple

mysql-password:
    default to crabapple

mysql-hostname:
    default to 127.0.0.1

mysql-port:
    default to 3306

mysql-db:
    default to crabapple

postgresql-username:
    default to crabapple

postgresql-password:
    default to crabapple

postgresql-hostname:
    default to 127.0.0.1

postgresql-port:
    default to 3306

postgresql-db:
    default to crabapple

'''


def work(args):
    try:
        opts, args = getopt.getopt(args, 'h:p:ds:c:', ['host=', 'port=', 'daemon',
                                                       'spec=', 'logdir=', 'datadir=',
                                                       'admin', 'config=', 'store=',
                                                       'mysql-username=', 'mysql-password=',
                                                       'mysql-hostname=', 'mysql-port=',
                                                       'mysql-db=',
                                                       'postgresql-username=', 'postgresql-password=',
                                                       'postgresql-hostname=', 'postgresql-port=',
                                                       'postgresql-db='])
    except getopt.GetoptError, e:
        raise InvalidArgsException(e)

    host = '127.0.0.1'
    port = 50000
    daemon = False
    spec_files = set()
    logdir = None
    datadir = None
    admin = False
    config_file = None
    store = None
    c = None
    mysql_username = None
    mysql_password = None
    mysql_hostname = None
    mysql_port = None
    mysql_db = None
    postgresql_username = None
    postgresql_password = None
    postgresql_hostname = None
    postgresql_port = None
    postgresql_db = None
    for o, a in opts:
        if o in ('-h', '--host'):
            host = a
        elif o in ('-p', '--port'):
            port = int(a)
        elif o in ('-d', '--daemon'):
            daemon = True
        elif o in ('-s', '--spec'):
            spec_files.add(a)
        elif o in ('--logdir',):
            logdir = a
        elif o in ('--datadir',):
            datadir = a
        elif o in ('--admin',):
            admin = True
        elif o in ('-c', '--config'):
            config_file = a
        elif o in ('--store',):
            store = a
        elif o in ('--mysql-username',):
            mysql_username = a
        elif o in ('--mysql-password',):
            mysql_password = a
        elif o in ('--mysql-hostname',):
            mysql_hostname = a
        elif o in ('--mysql-port',):
            mysql_port = int(a)
        elif o in ('--mysql-db',):
            mysql_db = a
        elif o in ('--postgresql-username',):
            postgresql_username = a
        elif o in ('--postgresql-password',):
            postgresql_password = a
        elif o in ('--postgresql-hostname',):
            postgresql_hostname = a
        elif o in ('--postgresql-port',):
            postgresql_port = int(a)
        elif o in ('--postgresql-db',):
            postgresql_db = a

    if config_file is not None:
        # Try to load from user-defined configuration file
        c = ServerConfig.load_from_file(config_file)
        if c is None:
            raise InvalidArgsException('Failed to load your configuration file')
    else:
        c = ServerConfig()

    # Update options from the command line
    if host is not None:
        c.host = host
    if port is not None:
        c.port = port
    if daemon:
        c.daemon = daemon
    if spec_files:
        c.specs = list(spec_files)
    if logdir is not None:
        c.logdir = logdir
    if datadir is not None:
        c.datadir = datadir
    if admin:
        c.admin = admin
    if store is not None:
        c.store = store
    if mysql_username is not None:
        c.store_mysql['username'] = mysql_username
    if mysql_password is not None:
        c.store_mysql['password'] = mysql_password
    if mysql_hostname is not None:
        c.store_mysql['hostname'] = mysql_hostname
    if mysql_port is not None:
        c.store_mysql['port'] = mysql_port
    if mysql_db is not None:
        c.store_mysql['db'] = mysql_db
    if postgresql_username is not None:
        c.store_postgresql['username'] = postgresql_username
    if postgresql_password is not None:
        c.store_postgresql['password'] = postgresql_password
    if postgresql_hostname is not None:
        c.store_postgresql['hostname'] = postgresql_hostname
    if postgresql_port is not None:
        c.store_postgresql['port'] = postgresql_port
    if postgresql_db is not None:
        c.store_postgresql['db'] = postgresql_db

    if not c.specs:
        raise InvalidArgsException('No spec specified')

    c.logdir = os.path.abspath(c.logdir)
    c.datadir = os.path.abspath(c.datadir)
    logfile = c.logdir + '/' + 'crabapple.log'
    logger = get_logger(logfile)
    s = Server(logger=logger, config=c)
    s.start()
