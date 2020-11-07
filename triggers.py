import re

match_triggers = (
    (re.compile("(hey|hi|hello|howdy|yo|greetings)"), "hello"),
    (re.compile("define"), "define"),
)


search_triggers = (
    (re.compile("weather"), "weather"),
    (re.compile("joke"), "joke"),
    (re.compile("(bitcoin[?]|ethereum[?]|litecoin[?]|xrp[?])"), "crypto"),
    (re.compile("(tide|tides)"), "tide")
)


def get_response_key(command, regex_type='match'):
    regex = re.match if regex_type == 'match' else re.search
    lookup = match_triggers if regex_type == 'match' else search_triggers
    for key, value in lookup:
        if regex(key, command):
            return value
    return None
