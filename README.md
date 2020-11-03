## Casper - The friendly Slack Bot
Casper is a slack bot written in Python and optimised to run in Docker/Kubernetes. It was developed as a bit of an educational project.
Since Slack RTM (real time messaging) is out of date and due to be decommissioned, this bot uses even subscription.
Credit to Robert Coleman (https://medium.com/@rdcolema7) for his great article on Slack frameworks, which this is based on.

# Slack Config

To use this you must first create an application on your slack workspace here: https://api.slack.com/apps, give it a name & then assign the OAuth permissions of chat:write & channels:history permissions. Then deploy the app to your workspace and make a note of the token.

# Bot Code

The bot is written in Python and is work in progress. A Flask app runs, which listens at the endpoint /slack/events. This is where Slack will send the events we subscribe to. In this case, messages. This is laid out in main.py by way of the following function:
```
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
```
This pulls the payload in from the Slack based on the event subscription 'messages', then split the relevant information into variables for use later. The important part we're looking for here is `text` which contains the body of the message. Later in this function we're checking whether the text sent by the Slack user contains the bot's name (in this case Casper) - It means the bot will only respond if addressed directly. 

We then assess whether the text after the bots name contains a command and if so, return the response to be sent back to the Slack Channel the message came from. This is done by `handle_command()` function, which in turn uses regex searches in `triggers.py` to work out whether the command sent in the body of the message, relates to a command the bot has to handle.

For example, if `@casper hey` is sent in the channel, it would be captured by the following:
```
match_triggers = (
    (re.compile("(hey|hi|hello|howdy|yo|greetings)"), "hello"),
    (re.compile("define"), "define"),
)
```
'hey' matches one of the keywords assigned to 'hello' and as such, 'hello' is returned as the keyword for the command.

This is handled by the `get_response_key()` function. Once we have the 'hello' keyword, the response dictionary in `resp_map.py` contains a list of responses to be sent back to the user, of which one is randomly chosen and returned to the user. Alternatively, if the command was not decided to be 'hello', it may relate to a response function, in which case the response dictionary would refer to one of the response functions in `responses.py`. These functions do the meat of the work in deciding which response to send back to the user and are pretty self explanatory. 

New functions can be added easily by adding a function to `responses.py` and simply adding the keyword(s) to `triggers.py` and the response function to `resp_map.py`.

# Docker

In the repo you'll find a Dockerfile to containerise this app. Since the app its self just sits there waiting for events to come in from Slack, it's an ideal candidate for a containerised application, or a cloud function depending on how hip you are. I wanted to run this locally, and since I have minikube running on my dev machine, I thought I'd have a tinker and see where we end up.

I won't explain the Dockerfile more than that, it's a very simple implementation running on `python:3.8.5-slim-buster`.

# Kubernetes

As I mentioned, I'm running minikube on my machine and thought I'd just throw this in there to run out of the way. As such I've included my K8s manifests. Again, really simple manifests which work fine for me. Your mileage may vary, feel free to edit as you wish.

# Ngrok

Included in the repo is a Dockerfile & K8s manifests for Ngrok. You may not need these, but as I was running this on my local machine I needed it to be able to get Slack talking to the bot. Everything is configured as standard, and should work out of the box with the manifests provided.
