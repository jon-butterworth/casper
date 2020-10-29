# #
# from requests import Request, Session
# from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
# import json
# import datetime
# import os

# url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest'
# parameters = {
#   'symbol': 'BTC',
#   'convert':'USD'
# }
# headers = {
#   'Accepts': 'application/json',
#   'X-CMC_PRO_API_KEY': '2c16eea9-e3a1-421c-bbd7-0e9bd91832d0',
# }
#
# session = Session()
# session.headers.update(headers)
#
#   response = session.get(url, params=parameters)
#   data = json.loads(response.text)
#   price = data['data']['BTC']['quote']['USD']['price']
#   return f'The current price of BTC is ${price:.2f}'
# except (ConnectionError, Timeout, TooManyRedirects) as e:
#   print(e)
#

## Import modules
import os
import datetime
import json
from requests import Request, Session

## Function to calculate a list of working dates between two dates
def workdays(d, end, excluded=(6, 7)): # Accept start date, end date & exclude weekends.
  days = [] # Creating an empty list to store the dates
  while d.date() <= end.date()): # If the start date is less than the end date...
    if d.isoweekday() not in excluded: # check if it's a week day (in python dates are assigned number 1-7, thus 6 & 7 are sat/sun
        days.append(d) # Add the date to the list.
    d += datetime.timedelta(days=1) # Carry on through the loop, timedelta finds the number of days between two dates.
    return days # Return the list of dates.

## Get the date from the API endpoint.
url = 'https://www.alphavantage.co/query?apikey=demo&function=TIME_SERIES_DAILY_ADJUSTED&symbol=MSFT'
session = Session()
output = session.get(url)
data = json.loads(output.text)

## Extract the symbol if needed - Looked at extracting the date, but it doesn't seem to be needed.
symbol = data['Meta Data']['2. Symbol']
date = data['Time Series (Daily)']

days_ago = os.environ['DAYS_AGO'] # Read in the environment variable for N days
today = datetime.datetime.now() # Work out todays date
today_date = today.strftime("%Y-%m-%d") # Format todays date to match the output of the API
past_date = today_date - datetime.timedelta(days=days_ago) # Calculate what the date would have been N number of days ago

days = workdays(past_date, today_date)

for day in days:
  print(data['Time Series (Daily)'][day]['4. close''])
