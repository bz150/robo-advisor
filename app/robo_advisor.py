# this is the "app/robo_advisor.py" file

import requests
import json

def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71


#
# PROGRAM INPUTS
#

request_URL = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&apikey=demo"
    # website > documentation > JSON first link

response = requests.get(request_URL)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #status code of the request #> 200
#print(response.text) #actual text of the request #> bunch string version of dictionaries
#    # need to parse this from strings into dictionary

parsed_response = json.loads(response.text)
#print(type(parsed_response)) #> dict
    # 2 keys: "Meta Data" and "Time Series (Daily)"
    # meta data is another dict
#print(parsed_response["Meta Data"].keys()) #> ['1. Information', '2. Symbol', '3. Last Refreshed', '4. Output Size', '5. Time Zone']
#print(parsed_response["Time Series (Daily)"].keys()) #> a bunch of dates; e.g. '2021-02-19'

# latest day
last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

# latest close, high, low
tsd = parsed_response["Time Series (Daily)"] # time series daily, for convenience. keys are all the dates

# convert the tsd keys (bunch of dates) into a list to have most recent date
dates = list(tsd.keys()) # CAN SORT TO ENSURE LATEST DAY IS FIRST
latest_day = dates[0]
latest_close = tsd[latest_day]['4. close']


#breakpoint()

#
# OUTPUT REQUIREMENTS
#
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") # USE DATE TIME MODULE
print("-------------------------")
print("LATEST DAY:", last_refreshed) # DOES NOT INCLUDE TIME ANYMORE
print("LATEST CLOSE:", to_usd(float(latest_close)))
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")