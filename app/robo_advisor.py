# this is the "app/robo_advisor.py" file

import requests
import json
import csv
import os
import string

from dotenv import load_dotenv
load_dotenv()

import datetime as dt
now = dt.datetime.now()

import pandas as pd
from pandas import DataFrame
import plotly.express as px


def to_usd(my_price):
    """
    Converts a numeric value to usd-formatted string, for printing and display purposes.
    Param: my_price (int or float) like 4000.444444
    Example: to_usd(4000.444444)
    Returns: $4,000.44
    """
    return f"${my_price:,.2f}" #> $12,000.71

def has_numbers(string):
    return any(char.isdigit() for char in string)
    # attribution: https://stackoverflow.com/questions/19859282/check-if-a-string-contains-a-number


#
# PROGRAM INPUTS
#

# customize URL to pull data
API_KEY = os.environ.get("ALPHAVANTAGE_API_KEY")

active = True
while active == True:
    ticker = input("Please enter a stock ticker: ")
    ticker = ticker.upper()

    if has_numbers(ticker) == True:
        print("Uh oh, it looks like there are some numbers in your ticker. Please retry with a properly formed ticker.")
        active = True
    elif len(ticker) > 5:
        print("Uh oh, it looks like your ticker is too long. Please retry with a properly formed ticker.")
        active = True
    elif ticker.isalpha() == False:
        print("Uh oh, it looks like your ticker has special characters. Please retry with a properly formed ticker.")
        active = True
    else:
        active = False

try:

    request_URL = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
        # website > documentation > JSON first link
    request_URL_weekly = f"https://www.alphavantage.co/query?function=TIME_SERIES_WEEKLY&symbol={ticker}&apikey={API_KEY}"
    
    response = requests.get(request_URL)
    response_2 = requests.get(request_URL_weekly)
    
    parsed_response = json.loads(response.text)
    parsed_response_2 = json.loads(response_2.text)
    
    # latest day
    last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]

    # latest close
    tsd = parsed_response["Time Series (Daily)"] # time series daily, for convenience. keys are all the dates
    tsw = parsed_response_2["Weekly Time Series"] # time series weekly, for 52-wk high/low calc. keys are all the dates
    
    # convert the tsd keys (bunch of dates) into a list to have most recent date
    dates = list(tsd.keys())
    latest_day = dates[0]
    latest_close = tsd[latest_day]['4. close']

    # 52-wk high and low
    # max of the high prices and min of the low prices in the last 52 weeks
    weeks = list(tsw.keys())

    fifty_two_weeks = []
    for i in range (0,52):
        fifty_two_weeks.append(weeks[i])    

    high_prices = []
    low_prices = []
    for i in fifty_two_weeks:
        high_prices.append((float(tsw[i]["2. high"])))
        low_prices.append((float(tsw[i]["3. low"])))
    recent_high = max(high_prices)
    recent_low = min(low_prices)


    #
    # RECOMMENDATION ALGORITHM
    #
    
    latest_close = float(latest_close)
    recent_high = float(recent_high)
    recent_low = float(recent_low)
    if latest_close > 1.2*(recent_low+recent_high)/2:
        recommendation = "BUY!"
        thesis = "Stock looks like it's trending up."
    elif latest_close < 0.8*(recent_low+recent_high)/2:
        recommendation = "SELL!"
        thesis = "Stock looks like it's headed down from here."
    else:
        recommendation = "Wait/hold..."
        thesis = "No conclusive evidence could be found to justify a buy or a sell."

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
    print("52-WK HIGH:", to_usd(float(recent_high)))
    print("52-WK LOW:", to_usd(float(recent_low)))
    print("-------------------------")

    # design algorithm
    print("RECOMMENDATION:", recommendation)
    print("RECOMMENDATION REASON:", thesis)
    print("-------------------------")

    # write data to csv
    csv_file_path = os.path.join(os.path.dirname(__file__),"..","data",ticker+" prices.csv") # relative filepath
    csv_headers = ["timestamp","open","high","low","close","volume"]
    with open(csv_file_path, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=csv_headers)
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
except:
    print("Hm, it seems like we can't find that ticker, sorry!")
    exit()


#
# PLOTTING CHART
# attribution: https://stackoverflow.com/questions/42372617/how-to-plot-csv-data-using-matplotlib-and-pandas-in-python
# attribution: https://colab.research.google.com/drive/1mSRkZSI_a0ASFSxOUzzLqFI21KDmH10w?usp=sharing
# attribution: https://plotly.com/python/line-charts/

# price (daily close) line graph
df = pd.read_csv(csv_file_path)
fig = px.line(df, x="timestamp", y="close", title=ticker+' Stock Price')
fig.show()

# volume bar graph
fig2 = px.bar(df, x="timestamp", y="volume", title=ticker+' Trading Volume')
fig2.show()