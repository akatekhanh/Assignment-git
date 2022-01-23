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
        self.asset_portfolio.add( Cash(100.01) )
        
        return self
        # try:
        #     assert self.are_equal( self.asset_portfolio.value(), 1800 )
        
        # except AssertionError:
        #     print('Test 1 Failed, Expected Value:' + '\t' + '1800' + ',\t' + 'Actual Value: \t' + str(portfolio.value()) + '\n')
     
    def are_equal( self, d1:float, d2:float ):
        return abs(d1-d2) < 0.0001

    
    def value_asset(self,date: str, currency_code:str, is_print=False):
        if currency_code != 'EUR':
            data = Program.get_history_FX_rate(date, currency_code)
            exchange_rate = data.get('rates', {}).get(currency_code)
        else: 
            exchange_rate = 1

        assets = self.consolidate_asset()
        total_assets = assets['cash']
        
        for key in assets['stock'].keys():
            total_assets += assets['stock'][key][2]
        
        result = total_assets*exchange_rate
        if is_print:
            print(f"Total assets in {date}: {result} ({currency_code})")
        return result

    
    def consolidate_asset(self):
        assets = {
            'cash': 0.0,
            'stock': {}
        }
        for item in self.asset_portfolio.portfolio:
            if isinstance(item, Cash):
                assets['cash'] += item.amount
            
            else:
                if not assets.get('stock').get(item.symbol):
                    assets['stock'][item.symbol] = [item.shares, item.price, item.shares*item.price]
                else:
                    assets['stock'][item.symbol][0] += item.shares
                    assets['stock'][item.symbol][1] += item.price
                    assets['stock'][item.symbol][2] += item.shares*item.price

        print(f"Cash: {assets['cash']} (EUR)")
        for key in assets['stock'].keys():
            shares = assets['stock'][key][0]
            avg_price = assets['stock'][key][2]/assets['stock'][key][0]
            print(f"{shares} shares of {key} stock at {avg_price} EUR")

        return assets

    
    def plot_the_change_in_value(self, year:str, currency_code:str):
        start = datetime(year, 1, 1)
        end = datetime(year, 1, 10)
        step = timedelta(days=1)
        result_time = []

        while start < end:
            result_time.append(start.strftime('%Y-%m-%d'))
            start += step
        
        data = {}
        for date in result_time:
            data[date] = self.value_asset(date, currency_code, False)
        
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

    ##########################################
    # TODO: task 2 -> Program.get_history_FX_rate
    ##########################################
    # TODO: task 3a -> utils.get_currency_code
    ##########################################
    # TODO: task 4, let run: python task_4.py
    ##########################################
    # TODO: task 5: uncomment to run
    # asset_portfolio.value_asset(
    #     date='2019-02-02',
    #     currency_code='VND',
    #     is_print=True
    # )
    ##########################################
    # TODO: task 6: 
    # asset_portfolio.consolidate_asset()
    ##########################################
    # TODO: task 7:
    # asset_portfolio.plot_the_change_in_value(
    #     year=2019,
    #     currency_code='EUR'
    # )
    ##########################################
    # TODO: task 8
    asset_portfolio.prove_historically_FX_rate()
    ##########################################
