import requests
import psycopg2
import pandas as pd

from bs4 import BeautifulSoup


MENU_URI = "https://mymall.se/inredning-mobler/barnrummet/belysning"

data = []
uri_response = requests.get(url=MENU_URI).content
bs_obj = BeautifulSoup(markup=uri_response, parser='html.parser', features='lxml')

debug = True
