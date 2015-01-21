# Copyright 2014 The crabapple Authors. All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


import logging

logger = None


def get_logger(logfile=None):
    global logger
    if logger is None:
        logger = logging.Logger('crabapple')
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        if logfile is not None:
            fh = logging.FileHandler(logfile)
        else:
            fh = logging.StreamHandler()
        fh.setFormatter(formatter)
        fh.setLevel(logging.INFO)
        logger.addHandler(fh)

    return logger
