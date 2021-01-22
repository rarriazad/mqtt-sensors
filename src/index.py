#!/usr/bin/python
# -*- coding: utf-8 -*

from modules import logger
from modules import setLevel
from modules import subscribe
from modules import read_config
from modules import save_config
#from modules import temperature
from modules import slackwc

from dotenv import load_dotenv
from datetime import datetime
from datetime import timedelta
from io import open

import subprocess
import argparse
import signal
import json
import time
import glob
import sys
import os
import re

##
#

def signal_handle(signum, frame):
    logger.info("sigterm received (%d)", signum)
    sys.exit(0)

##
#

def main():
 
    read_config()
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

    args = parser.parse_args()
    name = args.name

    load_dotenv()

    log_level = os.getenv("LOG_LEVEL", "info").lower()
    setLevel(args.verbose or log_level == 'debug')

    mqtt_host = args.mqtt_host or os.getenv("MQTT_HOST")
    mqtt_port = args.mqtt_port or os.getenv("MQTT_PORT")
    mqtt_user = args.mqtt_user or os.getenv("MQTT_USER")
    mqtt_pass = args.mqtt_pass or os.getenv("MQTT_PASS")

    mqtt_topic_req = args.mqtt_topic_req or os.getenv('MQTT_TOPIC_REQ')
    mqtt_topic_res = args.mqtt_topic_res or os.getenv('MQTT_TOPIC_RES')

    topic_req = f"{mqtt_topic_req}/{name}"
    topic_res = f"{mqtt_topic_res}/{name}"
    
    logger.debug("Starting MQTT")

    nextConnectionAt = datetime.now()
    connected = False

    HOME = os.getenv("HOME")

    pattern = re.compile(r'^Modify: (.*)\n')

    while True:

        now = datetime.now()

        if not connected and now > nextConnectionAt:
            try:
                
                @subscribe(topic_req, {"host": mqtt_host, "port": int(mqtt_port), "user": mqtt_user, "pass": mqtt_pass})
                def message_handle(payload, emit):
                    
                    try:
                        if 'id' not in payload:
                            raise Exception("request id is not present")
                            
                        if 'command' not in payload:
                            raise Exception("command is not present")

                        command = payload['command']

                        if command == 'config':

                            logger.debug("Config Temperature %s", {
                                'id': payload['id'],                            
                                'status':'Config max temperature',
                                'data':{
                                    'temp':payload['temp']
                            }})

                           
                            emit(topic_res, {
                                'id': payload['id'],                            
                                'status':'Config max temperature',
                                'data':{
                                    'temp':payload['temp']
                                }
                            })

                            try:
                                newTemp = payload['temp']
                                data = {"temp_max": newTemp}

                                save_config(data)
                                #updateTemperature('.local/config/hackrf-sensors.json', 0, '{"temp_max":' + newTemp + "}")

                            except Exception as ex:
                                logger.warning("%s", payload)
                                logger.error(ex)

                                emit(topic_res, {'id': payload['id'], 'error': ex})
                            
                          
                        elif command == 'status':
                            
                            #INTEGRAR PROCESO QUE OBTIENE T° DE LA MAQUINA
                            # Y PASARLO COMO VARIABLE A EMIT(TOPIC_RES)

                            logger.debug("Getting sensors data")
                     
                            emit(topic_res, {
                                'id': payload['id'],                            
                                'status':'Data sensors found',
                                'data':{
                                    'temp':payload['temp']
                                }
                            })

                        else:
                            emit(topic_res, {'id': payload['id']})

                    except Exception as ex:
                        logger.warning("%s", payload)
                        logger.error(ex)

                        emit(topic_res, {'id': payload['id'], 'error': ex})

                logger.info("mqtt connected")
                connected = True

            except Exception as ex:
                logger.error(ex)

                connected = False
                nextConnectionAt = now + timedelta(seconds=10)

                logger.debug("Reconnecting mqtt at 10 seconds")
        
        #data = temperature.getHighTemperature()
        #logger.info("temperature: %s", data)
        time.sleep(10)

        #idea para la notificacion
        
        # arbir json de la tempetatura
        #f = open('hackrf-sensors.json',) 

        # obtencion de los valor del json
        #data = json.load(f) 

        #cpu = data['temp_cpu'] # a reemplazar por valor real de la cpu via json 
        #temp = data['temp_max']
        #if cpu > temp:
            #slackwc.chat()

        text = 'hola'
        slackwc.chat()
            
##
#

if __name__ == '__main__':
    main()
