import os
import requests
from bs4 import BeautifulSoup as bs
from textblob import Word
from pyowm import OWM
# from pathlib import Path
# from dotenv import load_dotenv
import json
from requests import Request, Session

import nltk
nltk.download('wordnet')

# env_path = Path('') / '.env'
# load_dotenv(dotenv_path=env_path)


def check_weather(command):
    fluff_words = ['in', 'over', 'on', 'like']
    command = command.replace("?", "").split('weather')[1].split()
    command = ",".join(filter(lambda x: x not in fluff_words, command))

    if len(command.strip()) <= 1:
        command = 'Exeter'

    owm = OWM(os.environ['PYOWM_KEY'])
    w = owm.weather_manager().weather_at_place(command).weather
    report = "It's {temp} degrees and I would describe the condition as {condition}.".format(
        temp=w.temperature('celsius')["temp"], condition=w.detailed_status)
    return report


def define(command):
    word = command.split('define')[1].split()
    word = ", ".join(word)
    return Word(word).definitions[0]


def joke(_):
    url = requests.get('http://theoatmeal.com/djtaf/')
    soup = bs(url.content, 'lxml')
    random_joke = soup.find(class_='part1').get_text()
    random_answer = soup.find(id='part2_0').get_text()
    return "\n".join([random_joke, random_answer])

def crypto_coin_price(command):
    crypto_key = os.environ['CRYPTO_KEY']

    cryptos = ['bitcoin', 'litecoin', 'ethereum', 'xrp']
    for x in command.replace("?", "").split():
        if x in cryptos:
            crypto = x

    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
    parameters = {
        'slug': crypto,
        'convert': 'USD'
    }
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': crypto_key
    }
    session = Session()
    session.headers.update(headers)

    response = session.get(url, params=parameters)
    data = json.loads(response.text)
    for x in data['data'].values():
        price = x['quote']['USD']['price']

    return f'The current price of {crypto} is ${price:.2f}'
