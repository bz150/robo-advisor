# this is the "app/robo_advisor.py" file

import requests
import json
import csv
import os
from dotenv import load_dotenv
load_dotenv()
import datetime
now = datetime.datetime.now()

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

# customize URL to pull data
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")
ticker = input("Please enter a stock ticker: ")
ticker = ticker.upper()
request_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
    # website > documentation > JSON first link

response = requests.get(request_URL)
#print(type(response)) #> <class 'requests.models.Response'>
#print(response.status_code) #status code of the request #> 200
#print(response) #actual text of the request #> bunch string version of dictionaries
#print(type(response)) #actual text of the request #> bunch string version of dictionaries
#if "invalid API call" in response.text:
#    print("ERROR")


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

# recommendation algorithm
latest_close = float(latest_close)
recent_high = float(latest_close)
recent_low = float(latest_close)
if latest_close > 1.2*(recent_low+recent_high)/2:
    recommendation = "BUY!"
    thesis = "Stock looks like it's trending up!"
elif latest_close < 0.8*(recent_low+recent_high)/2:
    recommendation = "SELL!"
    thesis = "Stock looks like it's headed down!"
else:
    recommendation = "Wait/hold..."
    thesis = "No conclusive evidence could be found to justify a buy or a sell."


#breakpoint()

#
# OUTPUT REQUIREMENTS
#

# printing stock information
print("-------------------------")
print("SELECTED SYMBOL:", ticker)
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT:", now.strftime("%y-%m-%d %H:%M:%S"))
print("-------------------------")

# printing stock data
print("LATEST DAY:", last_refreshed) # DOES NOT INCLUDE TIME ANYMORE
print("LATEST CLOSE:", to_usd(float(latest_close)))
print("RECENT HIGH:", to_usd(float(recent_high)))
print("RECENT LOW:", to_usd(float(recent_low)))
print("-------------------------")

# design algorithm
print("RECOMMENDATION:", recommendation)
print("RECOMMENDATION REASON:", thesis)
print("-------------------------")

# write data to csv
csv_file_path = os.path.join(os.path.dirname(__file__),"..","data",ticker+" prices.csv") # relative filepath
with open(csv_file_path, "w") as csv_file:
    writer = csv.DictWriter(csv_file, fieldnames=["timestamp","open","high","low","close","volume"])
    writer.writeheader()

    # loop to write prices each date
    for day in dates:
        writer.writerow({
            "timestamp":day,
            "open":tsd[day]['1. open'],
            "high":tsd[day]['2. high'],
            "low":tsd[day]['3. low'],
            "close":tsd[day]['4. close'],
            "volume":tsd[day]['5. volume']
        })

print("Writing data to .csv file", csv_file_path)
print("-------------------------")

# conclusion
print("HAPPY INVESTING!")
print("-------------------------")