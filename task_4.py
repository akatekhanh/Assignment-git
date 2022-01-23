import os
from re import L
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
from dotenv import load_dotenv
from scipy.stats import zscore
load_dotenv()


BASE_URL = os.getenv('BASE_URL')
MY_KEY = os.getenv('MY_KEY')
WORLD_HAPPINESS_REPORT_URL = os.getenv('WORLD_HAPPINESS_REPORT_URL')
CURRENCY_CODE_URL = os.getenv('CURRENCY_CODE_URL')

def preprocess_and_merge_data(fx_change):
    world_happiness = pd.read_csv('data/world_happiness_report.csv')
    world_happiness['Country or Region'] = world_happiness['Country or Region'].str.lower()
    world_happiness_country_list = world_happiness['Country or Region'].to_list()
    currency_code = pd.read_csv('data/currency_code.csv')
    currency_code['Country'] = currency_code['Country'].str.lower().replace('\(', '').replace('\)', '')


    currency_code_merge = list()
    for index, row in currency_code.iterrows():
        if row['Country'] in world_happiness_country_list:
            merge_row = world_happiness[world_happiness['Country or Region'].astype(str).str.contains(row['Country'])]
            merge_row = merge_row.values.tolist()[0]
            merge_row.append(row['Code'])
            merge_row.append(fx_change[row['Code']])
            currency_code_merge.append(merge_row)


    return pd.DataFrame(currency_code_merge, columns=['Rank','Score','Country or Region','Code', 'Fx change'])

def build_fx_change_in_year(start: str, end: str, symbols: list):
    symbols_data = ','.join(symbols)
    start_fx_change = f'{BASE_URL}/{start}?access_key={MY_KEY}&symbols={symbols_data}'
    data_1 = requests.get(start_fx_change)
    data_1 = json.loads(data_1.content)

    end_fx_change = f'{BASE_URL}/{end}?access_key={MY_KEY}&symbols={symbols_data}'
    data_2 = requests.get(end_fx_change)
    data_2 = json.loads(data_2.content)

    fx_change = dict()
    for key in symbols:
        fx_change[key] = data_2['rates'].get(key, 0) - data_1['rates'].get(key, 0)

    return fx_change

def regression_model(data_point, label):
    label = np.array(label).reshape(-1,1)
    data_point = np.array(data_point).reshape(len(label),-1)
        
    model = LinearRegression()
    model.fit(data_point, label)
    return model

def polynomial_preprocess(X):
    poly = PolynomialFeatures(2)
    X = np.array(list(X)).reshape(-1,1)
    X_ = poly.fit_transform(X)
    return X_

def polynomial_process(X, y):
    y = np.array(list(y)).reshape(-1,1)
    X_ = polynomial_preprocess(X)
    model = regression_model(X_, y)
    return model

if __name__ == '__main__':
    currency_code = pd.read_csv('data/currency_code.csv')
    currency_code = currency_code.dropna()
    header = ['Base', 'Date', 'Timestamp']
    symbols = currency_code['Code'].to_list()
    fx_change = build_fx_change_in_year('2019-01-01', '2019-12-31', symbols)
    data = preprocess_and_merge_data(fx_change)
    fx_change_year = data['Fx change']
    score = data['Score']

    z_scores = zscore(data[['Fx change', 'Score']])
    filtered_entries = (np.abs(z_scores) < 1.5).all(axis=1)
    removed_outlier_data = data[filtered_entries]
    
    model_linear = regression_model(removed_outlier_data['Score'], removed_outlier_data['Fx change'])
    model_polynomial = polynomial_process(removed_outlier_data['Score'], removed_outlier_data['Fx change'])

    plt.plot(score, model_linear.predict(np.array(score).reshape(-1,1)).ravel(), 'b-', label='linear')
    plt.plot(score, model_polynomial.predict(polynomial_preprocess(score)).ravel(), 'g--', label='polynomial with degree 2')
    plt.plot(score, fx_change_year, 'ro')
    plt.xlabel('Happiness Score')
    plt.ylabel('Fx change in 2019')
    plt.axis([3, 8, -20, 20])
    plt.legend()
    if not os.path.isdir('imgs/'):
        os.mkdir('imgs/')
    plt.savefig('imgs/task4.png')
    plt.show()

    