# -*- coding: utf-8 -*

from .logger import logger

import json
import os

homedir = os.path.join(os.getenv("HOME", "./"), '.local/config')
filename = os.path.join(homedir, 'hackrf-sensors.json')

##
#

def read_config():

    if not os.path.isdir(homedir):
        os.makedirs(homedir)

    if os.path.isfile(filename):
        logger.debug("opening %s", filename)
        with open(filename, "r") as fd:
            data = json.load(fd)

    else:
        logger.debug("creating %s", filename)
        data = {
            "temp_max" : 75,
        }

        with open(filename, "w") as fd:
            json.dump(data, fd)

    return data

##
#

def save_config(data):

    logger.debug("updating data config [%s]", data)

    with open(filename, "r+") as fd:
        db = json.load(fd)
        logger.debug("data old [%s]", db)
        for key in data:
            if key in db:
                db[key] = data[key]

    with open(filename, "w") as fd:
        logger.debug("data new [%s]", db)
        json.dump(db, fd)

