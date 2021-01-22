# -*- coding: utf-8 -*

from dotenv import load_dotenv
from slack import WebClient
from slack.errors import SlackApiError
from modules import logger

import os

load_dotenv()

SLACK_TOKEN = os.getenv("SLACK_TOKEN") #token del bot/app
SLACK_CHANNEL = os.getenv("SLACK_CHANNEL") #canal donde sera "invocado"
SLACK_USERNAME = os.getenv("SLACK_USERNAME") #nombre del bot/app 

client = WebClient(token=SLACK_TOKEN)

#funcion para el envio del mensaje
def chat(data):
    
    try:

        res = client.chat_postMessage(
            username=SLACK_USERNAME,
            channel=SLACK_CHANNEL,
            text= "Cuidado la CPU ha superado el umbral de seguridad, la temperatura actual es de: " + str(data)#no es necesario un str para un int + " °C" #mensaje de prueba
        )

        logger.debug(res)

    except SlackApiError as ex:
        logger.error(ex)