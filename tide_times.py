from requests import Session
import json
import dateutil.parser
from datetime import datetime

headers = {
    'Ocp-Apim-Subscription-Key': 'a9826533aaee44a099999d698b74f93d',
}
station_id = '0026'

url = f'https://admiraltyapi.azure-api.net/uktidalapi/api/V1/Stations/{station_id}/TidalEvents'

session = Session()
session.headers.update(headers)

output = session.get(url)
data = json.loads(output.text)

today_idx = []
for i in range(5):
    date = dateutil.parser.parse(data[i]['Date']).date()
    if date == datetime.today().date():
        today_idx.append(i)

print(f'Tide times for {datetime.today().date().strftime("%d %B %Y")}:')
for tide in today_idx:
    event = data[tide]['EventType'] == 'LowWater' and 'Low tide' or data[tide]['EventType'] == 'HighWater' and 'Tigh tide'
    time = dateutil.parser.parse(data[tide]['DateTime']).time()
    height = round(data[tide]['Height'], 2)

    print(f'{event} is at {time} and will be {height}m')
