# -*- coding: utf-8 -*

from .logger import logger

import subprocess
import time
import re
import json
import calendar


def getHighTemperature():
    #Define linux command as 'cmd'
    cmd = "sensors | grep Core | sort -rn "

    #Example Output of subprocess: Core 0:        +65.0°C  (high = +100.0°C, crit = +100.0°C)
    output = subprocess.check_output(cmd, shell=True, encoding="utf-8")
    
    logger.debug("output: %s", output)

    #Parse output into List
    pattern = re.compile(r'.*:\s+.([0-9]+).*')
    for line in output.split("/n"):
        res = pattern.findall(line)
        logger.debug("Core Temperature found: %s",res)

    #Select Highes Value from list
    temp_cpu = (max(res))
    logger.debug("Max Temperature recorded: %s", temp_cpu)

    return int(temp_cpu)
    

def Saving_JSON():

    while True:
        temp_cpu = getHighTemperature()
        #json saving
        data = {}
        data['temperature_log'] = temp_cpu

        with open ('testjson.json', 'w') as f:
            json.dump(data,f)
        time.sleep(10)

