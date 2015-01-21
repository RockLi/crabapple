# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from crabapple.objects import Commit, Deployment, Base


class Store(object):

    def __init__(self, store_type, data_dir=None, **kwargs):
        assert store_type in ['memory', 'sqlite', 'mysql', 'postgresql']
        self.data_dir = data_dir
        self.store_type = store_type

        extra_args = {}
        if store_type == 'memory':
            connstr = 'sqlite://',
        elif store_type == 'sqlite':
            connstr = 'sqlite:///' + self.data_dir + '/' + 'crabapple.db'
        elif store_type == 'mysql':
            connstr = 'mysql://{0}:{1}@{2}:{3}/{4}'.format(kwargs.get('username', 'crabapple'),
                                                           kwargs.get('password', 'crabapple'),
                                                           kwargs.get('hostname', '127.0.0.1'),
                                                           kwargs.get('port', 3306),
                                                           kwargs.get('db', 'crabapple'))
            extra_args = {'encoding': 'utf8'}
        elif store_type == 'postgresql':
            connstr = 'postgresql://{0}:{1}@{2}:{3}/{4}'.format(kwargs.get('username', 'crabapple'),
                                                                kwargs.get('password', 'crabapple'),
                                                                kwargs.get('hostname', '127.0.0.1'),
                                                                kwargs.get('port', 5432),
                                                                kwargs.get('db', 'crabapple'))
            extra_args = {'encoding': 'utf8'}
        self.engine = create_engine(connstr, echo=True, **extra_args)
        self.Session = sessionmaker(bind=self.engine, expire_on_commit=False)
        self.specs = []
        self._s = None  # Session for InMemory Sqlite only

    def setup(self):
        Base.metadata.create_all(self.engine)

    def cleanup(self):
        pass

    @contextmanager
    def session_scope(self):
        if self.store_type != 'memory':
            session = self.Session()
            try:
                yield session
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.expunge_all()
                session.close()
        else:
            if self._s is None:
                self._s = self.Session()
            yield self._s

    def insert_commit(self, commit_object):
        with self.session_scope() as s:
            s.add(commit_object)

    def insert_deployment(self, deployment_object):
        with self.session_scope() as s:
            s.add(deployment_object)

        return deployment_object

    def update_deployment(self, deployment_object):
        with self.session_scope() as s:
            s.add(deployment_object)

    def get_deployment(self, deployment_id):
        with self.session_scope() as s:
            try:
                o = s.query(Deployment).filter(Deployment.id == deployment_id).one()
                return o
            except:
                return None

    def get_all_deployments(self):
        with self.session_scope() as s:
            return s.query(Deployment).all()

    def insert_spec(self, spec_object):
        if spec_object.id is None:
            spec_object.id = self.get_next_spec_id()
        self.specs.append(spec_object)
        return spec_object.id

    def get_next_spec_id(self):
        max_spec_id = 0
        for o in self.specs:
            if o.id > max_spec_id:
                max_spec_id = o.id

        return max_spec_id + 1

    def get_spec(self, spec_id):
        for o in self.specs:
            if o.id == spec_id:
                return o

        return None

    def get_all_specs(self):
        return self.specs

    def get_spec_by_name(self, name):
        for o in self.specs:
            if o.name == name:
                return o

        return None
