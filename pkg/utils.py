import requests
import json, csv
from lxml import html, etree
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime, timedelta

import os
from dotenv import load_dotenv
load_dotenv()
from pkg.files import save_csv_file
# from files import save_csv_file

MY_KEY = os.getenv('MY_KEY')
BASE_URL = os.getenv('BASE_URL')
WORLD_HAPPINESS_REPORT_URL = os.getenv('WORLD_HAPPINESS_REPORT_URL')
CURRENCY_CODE_URL = os.getenv('CURRENCY_CODE_URL')
DATA_PATH = os.getenv('DATA_PATH')


def get_history_FX_rate(header: list, symbols: list, is_save: bool, date:str):
    symbols_data = ','.join(symbols)
    url = f'{BASE_URL}/{date}?access_key={MY_KEY}&symbols={symbols_data}'
    data = requests.get(url)
    data = json.loads(data.content)

    if not is_save:
        return data
    result = {
        'Base': data['base'],
        'Date': data['date'],
        'Timestamp': datetime.utcfromtimestamp(data['timestamp']),
    }
    result.update(data['rates'])
    
    path = os.path.join(DATA_PATH, 'fx_rate_2019.csv')
    with open(path, 'a', newline='\n') as file:
        dictwriter_object = csv.DictWriter(file, fieldnames=header)

        if file.tell() == 0:
            dictwriter_object.writeheader()

        dictwriter_object.writerow(result)


def get_score_world_happiness_index():
    html_text = requests.get(WORLD_HAPPINESS_REPORT_URL).text
    html_xpath = html.fromstring(html_text)
    body_xpath = html_xpath.xpath('//*[@id="mw-content-text"]/div[1]/div[12]/table/tbody/tr[2]/td/table/tbody')

    header = ['Rank', 'Score', 'Country or Region']
    data = list()
    for tbody in body_xpath:
        for row in tbody.xpath("./tr"):
            tds = row.xpath("./td/text()")
            # Handle some rows missing data
            if tds:
                country = row.xpath("./td/a/text()")
                data.append([tds[0], tds[1], country[0]])

    # Write world happiness report to CSV file.
    save_csv_file(header=header, data=data, filename='world_happiness_report.csv')
    return pd.DataFrame(columns=header, data=data)

def get_currency_code():
    html_text = requests.get(CURRENCY_CODE_URL).text
    html_xpath = html.fromstring(html_text)
    body_xpath = html_xpath.xpath('/html/body/div[1]/div[2]/div/div/div/div/table/tbody')

    header = ['Country', 'Currency', 'Code', 'Number']
    data = list()
    for tbody in body_xpath:
        for row in tbody.xpath("./tr"):
            tds = row.xpath("./td/text()")
            data.append(tds)
    
    # Write currency code to CSV file.
    save_csv_file(header=header, data=data, filename='currency_code.csv')

    return pd.DataFrame(columns=header, data=data)


def get_history_FX_rate_in_year(year:int): 
    currency_code = pd.read_csv('data/currency_code.csv')
    currency_code = currency_code.dropna()
    header = ['Base', 'Date', 'Timestamp']
    symbols = currency_code['Code'].to_list()
    symbols = list(set(symbols))
    header.extend(symbols)
    start = datetime(year, 1, 1)
    end = datetime(year, 12, 31)
    step = timedelta(days=1)
    result_time = []
    while start < end:
        result_time.append(start.strftime('%Y-%m-%d'))
        start += step

    data = {}
    for date in result_time:
        get_history_FX_rate(header, symbols, True, date)

    # get_history_FX_rate(["USD","AUD","CAD","PLN","MXN"])
    # get_score_world_happiness_index()
    # get_currency_code()