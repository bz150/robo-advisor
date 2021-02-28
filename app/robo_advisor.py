# this is the "app/robo_advisor.py" file

import requests
import json
import csv
import os

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

# latest close
tsd = parsed_response["Time Series (Daily)"] # time series daily, for convenience. keys are all the dates

# convert the tsd keys (bunch of dates) into a list to have most recent date
dates = list(tsd.keys()) # CAN SORT TO ENSURE LATEST DAY IS FIRST
latest_day = dates[0]
latest_close = tsd[latest_day]['4. close']

# recent high and low
# max of the high prices provided, min of the low prices provided
high_prices = []
low_prices = []
for i in dates:
    high_prices.append((float(tsd[i]["2. high"])))
    low_prices.append((float(tsd[i]["3. low"])))
recent_high = max(high_prices)
recent_low = min(low_prices)

#breakpoint()

#
# OUTPUT REQUIREMENTS
#

# printing stock information
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm") # USE DATE TIME MODULE
print("-------------------------")

# printing stock data
print("LATEST DAY:", last_refreshed) # DOES NOT INCLUDE TIME ANYMORE
print("LATEST CLOSE:", to_usd(float(latest_close)))
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")

# design algorithm
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")


csv_file_path = os.path.join(os.path.dirname(__file__),"..","data","prices.csv") # relative filepath

with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["city","name"])
    writer.writeheader()
    writer.writerow({"city":"New York","name":"Yanks"})