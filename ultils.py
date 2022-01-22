import requests
import json
from bs4 import BeautifulSoup

my_key = '379637b6e070f320818a1f826ec4d469'
base_url = 'http://api.exchangeratesapi.io/v1/latest'
world_happiness_index_url = 'https://en.wikipedia.org/wiki/World_Happiness_Report#2019_report'

def get_history_FX_rate(symbols: list):
    symbols_data = ','.join(symbols)
    url = f'{base_url}?access_key={my_key}&symbols={symbols_data}'
    data = requests.get(url)

    print(json.loads(data.content))


def get_score_world_happiness_index():
    html = requests.get(world_happiness_index_url).text
    print(html)



# get_history_FX_rate(["USD","AUD","CAD","PLN","MXN"])
get_score_world_happiness_index()