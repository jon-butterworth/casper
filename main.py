import os
import random
import time

from slackclient import SlackClient
from response_map import response_dict
from triggers import get_response_key

BOT_NAME = "Casper"
slack_client = SlackClient(os.environ.get("SLACKBOT_TOKEN"))

def handle_command(command, channel):
    # Check for exact match first then check for keywords
    response_key = get_response_key(command, regex_type='match') or get_response_key(command, regex_type='search')

    # Default behaviour if no keys match command
    if not (response_key or command):
        response_key = 'no_command'
    elif not response_key:
        response_key = 'search'
        command = 'search' + command

    response = random.choice(response_dict[response_key])

    # If response is a function, call it with argument
    if callable(response):
        response = response(command)

    slack_client.api_call("chat.postMessage", channel=channel, text=response, as_user=True)

def parse_slack_output(slack_rtm_output):
    # Read data from the slack channel
    output_list = slack_rtm_output

    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output:
                text = output['text']

            # If casper is mentioned, take the text to the right of his name as the command.
            if BOT_NAME in text.lower():
                return text.lower().split(BOT_NAME)[1].strip().lower(), output['channel']

    return None, None

if __name__ == "__main__":
    if slack_client.rtm_connect():
        print("{BOT_NAME} now online.")

        while True:
            text_input, channel = parse_slack_output(slack_client.rtm_read())
            if text_input and channel:
                handle_command(text_input, channel)
            time.sleep(1) # Websocket read delay
        else:
            print("Connection failed.")
