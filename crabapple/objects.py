# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import arrow
import datetime
from sqlalchemy import (
    Column, Integer, String, DateTime, ForeignKey,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine


Base = declarative_base()


class DeploymentStatus(object):
    SCHEDULED = 0
    STARTED = 1
    SUCCESS = 2
    FAILED = 3


class Commit(Base):
    __tablename__ = 'commits'

    id = Column(Integer, primary_key=True)
    hash = Column(String)
    time = Column(DateTime)
    message = Column(String)
    url = Column(String)
    author_name = Column(String)
    author_email = Column(String)
    author_username = Column(String)
    committer_name = Column(String)
    committer_email = Column(String)
    committer_username = Column(String)

    def __repr__(self):
        return "<Commit(id='%s', hash='%s', 'author'='%s')>" % (self.id,
                                                                self.hash,
                                                                self.author_name)


class Deployment(Base):
    __tablename__ = 'deployments'

    id = Column(Integer, primary_key=True)
    spec_id = Column(Integer)
    branch = Column(String)
    status = Column(Integer)
    triggered_time = Column(DateTime)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    triggered_commit_id = Column(Integer, ForeignKey('commits.id'))
    pusher_name = Column(String)
    pusher_email = Column(String)

    triggered_commit = relationship("Commit", backref="Deployment", lazy="joined")

    def __repr__(self):
        return "<Deployment(id='%s', spec_id='%s', branch='%s')>" % (self.id,
                                                                     self.spec_id,
                                                                     self.branch)

    def mark_status(self, st):
        self.status = st

    def is_successful(self):
        return self.status == DeploymentStatus.SUCCESS

    def get_status_description(self):
        if self.status == DeploymentStatus.SCHEDULED:
            return 'scheduled'
        elif self.status == DeploymentStatus.STARTED:
            return 'started'
        elif self.status == DeploymentStatus.FAILED:
            return 'failed'
        elif self.status == DeploymentStatus.SUCCESS:
            return 'success'

    @staticmethod
    def parse_from_github(payload, store):
        print store

        assert isinstance(payload, dict)

        ref = payload['ref']
        branch = ref.split('/')[-1]

        d = Deployment(status=DeploymentStatus.SCHEDULED,
                       triggered_time=datetime.datetime.now())
        d.branch = branch
        d.pusher_name = payload['pusher']['name']
        d.pusher_email = payload['pusher']['email']

        phc = payload['head_commit']
        head_commit = Commit()
        head_commit.hash = phc['id']
        head_commit.time = phc['timestamp']
        head_commit.message = phc['message']
        head_commit.url = phc['url']
        head_commit.author_name = phc['author']['name']
        head_commit.author_email = phc['author']['email']
        head_commit.author_username = phc['author']['username']
        head_commit.committer_name = phc['committer']['name']
        head_commit.committer_email = phc['committer']['email']
        head_commit.committer_username = phc['committer']['username']
        head_commit.time = arrow.get(head_commit.time).datetime
        store.insert_commit(head_commit)

        d.triggered_commit_id = head_commit.id
        d.triggered_commit = head_commit
        return d
