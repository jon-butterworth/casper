import os
import requests
from bs4 import BeautifulSoup as bs
from textblob import Word
from pyowm import OWM
import json
from requests import Request, Session
import dateutil.parser
from datetime import datetime, timedelta
import nltk

nltk.download('wordnet', quiet=True)

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

def check_tides(command):
    tidal_stations = {
        'teignmouth': '0026', 'totnes': '0023C', 'torquay': '0025', 'exmouth': '0027'
    }

    fluff_words = ['time', 'times', 'for', 'in', 'at', 'tides', 'on']
    command = command.replace("?", "").split('tide')[1].split()
    command = ", ".join(filter(lambda x: x not in fluff_words, command))

    days = {
        'today': datetime.today().date(), 'tomorrow': datetime.today().date() + timedelta(days=1),
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6
    }

    for k, v in days.items():
        if isinstance(v, int) and k in command:
            delta = (v - datetime.today().weekday()) % 7
            day = datetime.today().date() + timedelta(days=delta)
        elif k in command:
            day = v

    for k, v in tidal_stations.items():
        if k in command:
            station_id = v
            location = k

    apikey = os.environ['TIDE_KEY']
    headers = {
        'Ocp-Apim-Subscription-Key': apikey,
    }

    url = f'https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/{station_id}/TidalEvents'

    session = Session()
    session.headers.update(headers)

    output = session.get(url)
    data = json.loads(output.text)

    idx = []
    for i in range(24):
        if dateutil.parser.parse(data[i]['Date']).date() == day:
            idx.append(i)

    output = []
    for tide in idx:
        event = data[tide]['EventType'] == 'LowWater' and 'Low tide' or data[tide][
            'EventType'] == 'HighWater' and 'High tide'
        time = str(dateutil.parser.parse(data[tide]['DateTime']).time().replace(second=0, microsecond=0))[:-3]
        height = round(data[tide]['Height'], 2)

        output.append(f'{event} is at {time} and will be {height}m')

    output.insert(0, f"Tide times in {location.title()} for {day.strftime('%d %B %Y')}:\n")
    print(location)
    result = "\n".join(output)
    return result
