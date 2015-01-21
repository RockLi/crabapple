# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import getopt
from crabapple.deploy import Deployer
from crabapple.exception import InvalidArgsException


help_msg = '''crabapple deploy --spec spec_file
'''


def work(args):
    try:
        opts, args = getopt.getopt(args, 's:', ['spec='])
    except getopt.GetoptError:
        raise InvalidArgsException()

    spec_file = None
    for o, a in opts:
        if o in ('-s', '--spec'):
            spec_file = a

    if spec_file is None:
        raise InvalidArgsException()

    deployer = Deployer(spec_file)
    deployer.do()
