# this is the "app/robo_advisor.py" file

import requests
import json

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

last_refreshed = parsed_response["Meta Data"]["3. Last Refreshed"]


#breakpoint()


#
# OUTPUT REQUIREMENTS
#
print("-------------------------")
print("SELECTED SYMBOL: XYZ")
print("-------------------------")
print("REQUESTING STOCK MARKET DATA...")
print("REQUEST AT: 2018-02-20 02:00pm")
print("-------------------------")
print("LATEST DAY:", last_refreshed) # DOES NOT INCLUDE TIME ANYMORE
print("LATEST CLOSE: $100,000.00")
print("RECENT HIGH: $101,000.00")
print("RECENT LOW: $99,000.00")
print("-------------------------")
print("RECOMMENDATION: BUY!")
print("RECOMMENDATION REASON: TODO")
print("-------------------------")
print("HAPPY INVESTING!")
print("-------------------------")