import os

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
