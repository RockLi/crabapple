# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import os
from functools import partial


def run(c):
    return os.system(c)


def script(filename):
    return partial(run, filename)


def cmd(c):
    return partial(run, c)
