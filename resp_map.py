import responses as rsp

resp_dict = {
    'define': [
        rsp.define
    ],
    'hello': [
        "Yo",
        "Hey",
        "Howdy",
        "Hello",
        "Hola"
    ],
    'joke': [
        rsp.joke
    ],
    'weather': [
        rsp.check_weather
    ],
    'crypto': [
        rsp.crypto_coin_price
    ],
    'tides': [
        rsp.check_tides
    ]
}
