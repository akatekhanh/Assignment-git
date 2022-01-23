# -*- coding: utf-8 -*-
import os
import requests
import json, csv
from datetime import datetime, timedelta
from asset_portfolio import AssetPortfolio
from exchange_rates import Cash
from stock import Stock
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib.dates as mdates

from dotenv import load_dotenv
from pkg.utils import get_currency_code, get_history_FX_rate, get_score_world_happiness_index
from task_4 import task4
load_dotenv()


MY_KEY = os.getenv('MY_KEY')
BASE_URL = os.getenv('BASE_URL')
WORLD_HAPPINESS_REPORT_URL = os.getenv('WORLD_HAPPINESS_REPORT_URL')
CURRENCY_CODE_URL = os.getenv('CURRENCY_CODE_URL')
DATA_PATH = os.getenv('DATA_PATH')

class Program(object):
    def __init__(self):
        """Init
        Args:
            exchange_rate (float): the exchange_rate of the portfolio
            date (str): date to value the portfolio (i.e: 2019-01-01)
        """
        self.asset_portfolio = AssetPortfolio()
    
    def main( self ):
        ''' SEE README FOR INSTRUCTIONS '''
        self.test1()
        
        input('Done...(Press any key)')
    

    def add_to_asset(self):
        self.asset_portfolio.add( Stock('ABC',200,4) )
        self.asset_portfolio.add( Stock('ABC',300,5) )
        self.asset_portfolio.add( Stock('DDW',100,10) )
        self.asset_portfolio.add( Cash(100.01, 'USD') )
        self.asset_portfolio.add( Cash(50.01, 'USD') )
        self.asset_portfolio.add( Cash(10.01, 'EUR') )
        
        return self
        # try:
        #     assert self.are_equal( self.asset_portfolio.value(), 1800 )
        
        # except AssertionError:
        #     print('Test 1 Failed, Expected Value:' + '\t' + '1800' + ',\t' + 'Actual Value: \t' + str(portfolio.value()) + '\n')
     
    def are_equal( self, d1:float, d2:float ):
        return abs(d1-d2) < 0.0001

    
    def value_asset(self,date: str, currency_code:str, data, is_print=False, index=0):
        currency_code_data = pd.read_csv('data/currency_code.csv')
        currency_code_data = currency_code_data.dropna()
        header = ['Base', 'Date', 'Timestamp']
        symbols = currency_code_data['Code'].to_list()
        symbols = ','.join(symbols)

        mode = 0
        if not data:
            data = Program.get_history_FX_rate(date, symbols)
            mode = 1


        total_assets = 0.0
        assets = self.consolidate_asset()
        # Convert from currency cash code to EUR cash
        for key in assets['cash'].keys():
            fx_rate = data.get(key)[index] if mode == 0 else data.get('rates', {}).get(key)
            total_assets += (1/fx_rate)*assets['cash'][key]
        
        # Convert from currency stock code to EUR cash
        for key in assets['stock'].keys():
            total_assets += assets['stock'][key][2]
        
        # convert the EUR to currency code
        fx_rate = data.get(currency_code)[index] if mode == 0 else data.get('rates', {}).get(currency_code)
        result = total_assets*fx_rate
        if is_print:
            print(f"Total assets in {date}: {result} ({currency_code})")
        return result

    
    def consolidate_asset(self, is_print=False):
        assets = {
            'cash': {},
            'stock': {}
        }
        for item in self.asset_portfolio.portfolio:
            if isinstance(item, Cash):
                if not assets['cash'].get(item.code):
                    assets['cash'][item.code] = item.amount
                else:
                    assets['cash'][item.code] += item.amount
            
            else:
                if not assets.get('stock').get(item.symbol):
                    assets['stock'][item.symbol] = [item.shares, item.price, item.shares*item.price]
                else:
                    assets['stock'][item.symbol][0] += item.shares
                    assets['stock'][item.symbol][1] += item.price
                    assets['stock'][item.symbol][2] += item.shares*item.price

        if is_print:
            for key in assets['cash'].keys():
                print(f"Amount of {key}: {assets['cash'][key]}")
            
            for key in assets['stock'].keys():
                shares = assets['stock'][key][0]
                avg_price = assets['stock'][key][2]/assets['stock'][key][0]
                print(f"{shares} shares of {key} stock at {avg_price} EUR")

        return assets

    
    def plot_the_change_in_value(self, year:str, currency_code:str):
        start = datetime(year, 1, 1)
        end = datetime(year, 12, 31)
        step = timedelta(days=1)
        result_time = []

        while start < end:
            result_time.append(start.strftime('%Y-%m-%d'))
            start += step
        
        csv_data = pd.read_csv('data/fx_rate_2019.csv')

        data = {}
        for index,date in enumerate(result_time):
            data_date = csv_data[csv_data['Date']==date].to_dict()
            data[date] = self.value_asset(date, currency_code, data_date, False, index)
        
        date = list(data.keys())
        values = list(data.values())

        fig = plt.figure(figsize = (10, 5))
 
        # creating the bar plot
        plt.bar(date, values, color ='maroon', width = 0.4)
        
        plt.xlabel("Date time")
        plt.ylabel(f"The change in value of our portfolio in {currency_code}")
        plt.title(f"The change in value of our portfolio in {year}")
        plt.show()
        

    @staticmethod
    def prove_historically_FX_rate():
        '''
            Notes: 
                Because of api call limitation, 
                I can only scrape data for 1 year then save it to csv file for later use. 
                if you want to scrapre more, please correct the number of days and comment this block code
        '''
        # Start block code
        # start = datetime(2020, 1, 1)
        # end = datetime(2020, 12, 31)
        # step = timedelta(days=1)
        # result_time = []

        # while start < end:
        #     result_time.append(start.strftime('%Y-%m-%d'))
        #     start += step
        # data_to_csv = []
        # header = ['Date', 'USDtoEUR']
        # for date in result_time:
        #     data = Program.get_history_FX_rate(date, 'USD')
        #     data_to_csv.append([date, 1/data.get('rates', {}).get('USD',0)])

        # path = os.path.join(DATA_PATH, 'USD_EUR.csv')
        # with open(path, 'w', newline='\n') as file:
        #     # Create CSV file
        #     writer = csv.writer(file)
        #     # Write the header
        #     writer.writerow(header)
        #     # Write the data
        #     writer.writerows(data_to_csv)
        # End block code

        df = pd.read_csv('data/USD_EUR.csv')
        ax = df.plot(x_compat=True, figsize=(10, 5), legend=None, ylabel='Counts')
        ax.set_ylim(*ax.get_ylim()) 

        xmin, xmax = ax.get_xlim()
        days = np.arange(np.floor(xmin), np.ceil(xmax)+2)
        weekends = [(dt.weekday()>=5)|(dt.weekday()==0) for dt in mdates.num2date(days)]
        ax.fill_between(days, *ax.get_ylim(), where=weekends, facecolor='k', alpha=.1)
        ax.set_xlim(xmin, xmax)

        plt.show()

    @staticmethod
    def get_history_FX_rate(date: str, currency_code: str, base='EUR'):
        try:
            url = f'{BASE_URL}/{date}?access_key={MY_KEY}&symbols={currency_code}'
            data = requests.get(url)
            data = json.loads(data.content)

        except Exception as e:
            print(e)
            raise "API call to http://api.exchangeratesapi.io have been some error!!!"
        
        return data


if __name__ == '__main__':
    
    asset_portfolio = Program().add_to_asset()

    choise = input("Input your task you want to implement (from 2 to 9): ")
    if choise == '2':
        ##########################################
        # TODO: task 2 -> Program.get_history_FX_rate
        today = datetime.today().strftime("%Y-%m-%d")
        currency_code = input("Input your currency code you want to scrape: ")
        print(Program.get_history_FX_rate(today, currency_code))
    
    elif choise == '3':
        ##########################################
        # TODO: task 3a -> utils.get_currency_code
        # Task 3a
        data_3a = get_currency_code()
        print(data_3a)

        # Task 3b
        data_3b = get_score_world_happiness_index()
        print(data_3b)
    
    elif choise == '4':
        ##########################################
        # TODO: task 4, let run this command: python task_4.py
        task4()
    
    elif choise == '5':
    ##########################################
        # TODO: task 5: uncomment to run
        currency_code = 'VND'
        asset_portfolio.value_asset(
            date='2019-02-03',
            currency_code='VND',
            data=None,
            is_print=True
        )
    
    elif choise == '6':
        ##########################################
        # # TODO: task 6: 
        asset_portfolio.consolidate_asset(is_print=True)
    
    elif choise == '7':
        ##########################################
        # TODO: task 7:
        asset_portfolio.plot_the_change_in_value(
            year=2019,
            currency_code='EUR'
        )
    
    elif  choise == '8':
        ##########################################
        # TODO: task 8
        asset_portfolio.prove_historically_FX_rate()
    
    elif choise == '9':
        ##########################################
        pass

    else:
        print("Your choise does not exist")