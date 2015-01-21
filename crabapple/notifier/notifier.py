# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

import abc


class Notifier(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def config(self, kwargs):
        pass

    @abc.abstractmethod
    def send(self, msg):
        pass
