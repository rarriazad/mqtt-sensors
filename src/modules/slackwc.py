# -*- coding: utf-8 -*

from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError
from logger import *

import os

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN") #token del bot/app
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL") #canal donde sera "invocado"
SLACK_USERNAME = os.getenv("SLACK_USERNAME") #nombre del bot/app 

client = WebClient(token=SLACK_TOKEN)

def chat():
    
    try:

        res = client.chat_postMessage(
            username=SLACK_USERNAME,
            channel=SLACK_CHANNEL,
            text= "Cuidado la CPU a superado el umbral de seguridad, la tempetura actual es de: " #+ "tem_cpu" + " °C" #mensaje de prueba, luego cambiar para mostrar más info de la CPU
        )

        logger.debug(res)

    except SlackApiError as ex:
        logger.error(ex)