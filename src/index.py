#!/usr/bin/python
# -*- coding: utf-8 -*

from modules import logger
from modules import setLevel

from dotenv import load_dotenv

import argparse
import signal
import sys

##
#

def signal_handle(signum, frame):
    logger.info("sigterm received (%d)", signum)
    sys.exit(0)

##
#

def main():

    signal.signal(signal.SIGINT,  signal_handle)
    signal.signal(signal.SIGTERM, signal_handle)

    parser = argparse.ArgumentParser()
    parser.add_argument("name")
    parser.add_argument("--verbose", action="store_true")
    parser.add_argument("--mqtt-host")
    parser.add_argument("--mqtt-port")
    parser.add_argument("--mqtt-user")
    parser.add_argument("--mqtt-pass")
    parser.add_argument("--mqtt-topic-req")
    parser.add_argument("--mqtt-topic-res")

    # agumentos para la api de slack #
 
    parser.add_argument('https://hooks.slack.com/services/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') # Token del bot

    args = parser.parse_args()

    load_dotenv()

    log_level = os.getenv("LOG_LEVEL", "info").lower()
    setLevel(args.verbose or log_level == 'debug')

##
#

if __name__ == '__main__':
    main()
