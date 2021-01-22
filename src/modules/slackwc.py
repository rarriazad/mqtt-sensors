# -*- coding: utf-8 -*
​
from dotenv import load_dotenv
​
from slack import WebClient
from slack.errors import SlackApiError
​
from .logger import logger
​
import os
​
SLACK_TOKEN = 'xoxb-305786002212-395782522743-K8nXYZJ5TfJqSY7KOEuykVsc' # os.getenv("SLACK_TOKEN")
SLACK_CHANNEL = '#practicas' #os.getenv("SLACK_CHANNEL") #canal donde sera "invocado"
SLACK_USERNAME = "Bot_Temp(T.leo)" #nombre del bot/app
​
client = WebClient(token=SLACK_TOKEN)
​
def chat(text):
    try:
​
        res = client.chat_postMessage(
            username=SLACK_USERNAME,
            channel=SLACK_CHANNEL,
            text= Temperatura 
        )
​
        logger.debug(res)
​
    except SlackApiError as ex:
        logger.error(ex)