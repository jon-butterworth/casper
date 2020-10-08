import os
import requests

from bs4 import BeautifulSoup
from textblob import Word
from pyown import OWM
from pyowm-utils import config
from pyown-utils import timestamp

def check_weather(command):
    fluff_words = ["in", "over", "like"]
    command = command.replace("?", "").split('weather')[1].split()
    command = ",".join(filter(lambda x: x not in fluff_words, command))

    if command.strip() <= 1:
        command = "exeter,gb"

    owm = OWM(os.environ.get('PYOWM_KEY'))
    w = owm.weather_manager().weather_at_place('command').weather
    report = "It's {temp} degrees and I would describe the condition as {condition}.".format(
        temp=w.temperature('celsius')["temp"], condition=w.detailed_report())
    return report

def define(command):
    word = Word(command.split("define")[1].split())
    return word.definitions[0]

def joke(_):
    url = requests.get('http://theoatmeal.com/djtaf/')
    soup = BeautifulSoup(url.content, 'lxml')
    random_joke = soup.find(class_='part1').get_text()
    random_answer = soup.find(id='part2_0').get_text()
    return "\n".join([random_joke, random_answer])
