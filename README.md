# robo-advisor
Robo advisor project for OPIM Python course
Original project instructions on [Github](https://github.com/prof-rossetti/intro-to-python/blob/master/projects/robo-advisor/README.md)

This project requires use of the [AlphaVantage Stock Market API](https://www.alphavantage.co/) to function properly and provide outputs.

Note that I am not a registered financial advisor, please do your own research before making investment decisions. The following is merely for fun!

## Initial Setup
Clone or download the [robo-advisor repo](https://github.com/bz150/robo-advisor) from GitHub. You may have to fork this first for your own usage.

To access, the program, you will first want to navigate to where it's saved through the command line. If on the desktop (recommended for simplicity), it would be `cd ~/desktop/robo-advisor`.

Next, you'll want to set up a virtual environment, which will allow you to use the program's features. Type this into the command line:
```
conda create -n stocks-env python=3.8
conda activate stocks-env
pip install -r requirements.txt
```

When it's time to run the program, type into the command line `python app/robo_advisor.py`. Note that the python file is under the app drawer, which may be different from past projects.

## Alpha Vantage API
To use the program, you will need to obtain an Alpha Vantage API key from their [webiste](https://www.alphavantage.co/). Once you receive it, set that equal to `ALPHAVANTAGE_API_KEY` in the `.env` file (e.g. `ALPHAVANTAGE_API_KEY = 123code`).

## Features
To see the .csv file that is saved after entering the ticker, navigate to the data drawer and look for the file with the ticker's name included.