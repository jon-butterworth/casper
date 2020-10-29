import os
import slack
import random
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from triggers import get_response_key
from resp_map import resp_dict

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adapter = SlackEventAdapter(os.environ['SIGN_SECRET'], '/slack/events', app)

client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']# clean this up - seems messy
BOT_NAME = '<@' + BOT_ID + '>' # clean this up - seems messy

def handle_command(command):
    response_key = get_response_key(command, regex_type='match') or get_response_key(command, regex_type='search')
    response = random.choice(resp_dict[response_key])

    # if not (response_key or command):
    #     response_key = 'no_command'
    # elif not response_key:
    #     response_key = 'search'
    #     command = 'search' + command

    if callable(response):
        response = response(command)

    return response


@slack_event_adapter.on('message')
def message(payload):
    event = payload.get('event', {})
    channel_id = event.get('channel')
    user_id = event.get('user')
    text = event.get('text')

    if BOT_ID in text:
        command = text.split(BOT_ID)[1].strip('>').lstrip().lower()
        response = handle_command(command)

        client.chat_postMessage(channel=channel_id, text=response)


if __name__ == "__main__":
    app.run(port=5000)
