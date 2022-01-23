import os
import pandas as pd
import matplotlib.pyplot as plt
import requests
import json
from dotenv import load_dotenv
load_dotenv()

BASE_URL = os.getenv('BASE_URL')
MY_KEY = os.getenv('MY_KEY')
WORLD_HAPPINESS_REPORT_URL = os.getenv('WORLD_HAPPINESS_REPORT_URL')
CURRENCY_CODE_URL = os.getenv('CURRENCY_CODE_URL')

fx_change = {'AFN': 0.9658069999999981, 'EUR': 0, 'ALL': -2.080030999999991, 'DZD': -1.799574000000007, 'USD': -0.0241340000000001, 'AOA': 187.35222900000002, 'XCD': -0.06522300000000003, 'ARS': 24.048150999999997, 'AMD': -17.486511999999948, 'AWG': -0.04344100000000006, 'AUD': -0.026853999999999933, 'AZN': -0.042735999999999885, 'BSD': -0.025222999999999995, 'BHD': -0.009082000000000034, 'BDT': -0.7069529999999986, 'BBD': -0.023508000000000084, 'BYN': -0.11010199999999992, 'BZD': -0.04349899999999973, 'XOF': 2.6251060000000734, 'BMD': -0.0241340000000001, 'BTN': 0.39023799999999653, 'INR': 0.0679930000000013, 'BOB': -0.1802279999999996, 'BOV': 0, 'BAM': 0.0015400000000000968, 'BWP': -0.410188999999999, 'NOK': -0.2048249999999996, 'BRL': 0.061797000000000324, 'BND': -0.294786, 'BGN': 0.015041000000000082, 'BIF': 61.44628599999987, 'CVE': 0.13416500000001008, 'KHR': -15.986713000000236, 'XAF': 0.48862000000008265, 'CAD': -0.10265600000000008, 'KYD': -0.017962000000000033, 'CLF': 0.001357999999999998, 'CLP': 34.19321600000001, 'CNY': -0.07086099999999984, 'COP': -38.152978000000076, 'COU': 0, 'KMF': -1.4502459999999928, 'CDF': 21.22486499999991, 'NZD': -0.037881000000000054, 'CRC': -49.64409699999999, 'HRK': 0.051442999999999905, 'CUC': -0.0241340000000001, 'CUP': -0.6395490000000024, 'ANG': -0.1364049999999999, 'CZK': -0.3035160000000019, 'DKK': 0.01021500000000053, 'DJF': -4.2886939999999925, 'DOP': 1.4760320000000036, 'EGP': -2.545618000000001, 'SVC': -0.18832800000000027, 'ERN': -0.3613970000000002, 'ETB': 3.6496680000000055, 'FKP': 0.017588999999999966, 'FJD': -0.05054800000000004, 'XPF': 0.6003309999999971, 'GMD': 0.9577559999999963, 'GEL': 0.13728600000000002, 'GHS': 0.7794509999999999, 'GIP': 0.017935999999999952, 'GTQ': -0.1918659999999992, 'GBP': -0.05258499999999999, 'GNF': 313.0822649999991, 'GYD': -4.725653999999992, 'HTG': 18.39295, 'HNL': -0.21739099999999922, 'HKD': -0.23973900000000015, 'HUF': 10.031999999999982, 'ISK': 2.4985149999999976, 'IDR': -996.1311839999998, 'XDR': -0.013743999999999978, 'IRR': -1016.1587960000033, 'IQD': -29.0059040000001, 'ILS': -0.40796199999999994, 'JMD': 2.4275900000000092, 'JPY': -3.7548280000000034, 'JOD': -0.017641999999999936, 'KZT': -11.152308000000005, 'KES': -3.0030629999999974, 'KPW': -21.791907000000037, 'KRW': 17.92333899999994, 'KWD': -0.00754699999999997, 'KGS': -2.063495000000003, 'LAK': 186.71418099999937, 'LBP': -32.268988000000036, 'LSL': -0.7736590000000003, 'ZAR': -0.7814000000000014, 'LRD': 30.197249999999997, 'LYD': -0.014944000000000068, 'CHF': -0.04030699999999987, 'MOP': -0.2277369999999994, 'MKD': -0.13829400000000192, 'MGA': 156.39202000000023, 'MWK': -63.299049999999966, 'MYR': -0.14626300000000025, 'MVR': -0.3835940000000022, 'MRU': 0, 'MUR': 1.445768000000001, 'XUA': 0, 'MXN': -1.260743999999999, 'MXV': 0, 'MDL': -0.30201100000000025, 'MNT': 48.753584000000046, 'MAD': -0.20065299999999908, 'MZN': -1.4890979999999985, 'MMK': -110.76800200000002, 'NAD': -0.77609, 'NPR': 0.6806110000000132, 'NIO': 0.7980110000000025, 'NGN': -8.87561199999999, 'OMR': -0.009164000000000005, 'PKR': 13.628338000000014, 'PAB': -0.025337000000000165, 'PGK': 0.10351899999999992, 'PYG': 419.640085, 'PEN': -0.14361200000000007, 'PHP': -3.361377999999995, 'PLN': -0.018036000000000385, 'QAR': -0.08818799999999971, 'RON': 0.13946600000000053, 'RUB': -9.365069000000005, 'RWF': 27.7783290000001, 'SHP': -0.031887, 'WST': -0.06129999999999969, 'STN': 0, 'SAR': -0.060380999999999574, 'RSD': -0.605165999999997, 'SCR': -0.26706899999999933, 'SLL': 1082.7385300000005, 'SGD': -0.04506399999999999, 'XSU': 0, 'SBD': -0.12407500000000127, 'SOS': -12.87527799999998, 'SSP': 0, 'LKR': -6.100775999999996, 'SDG': -3.824109, 'SRD': -0.18000400000000027, 'SZL': -0.721502000000001, 'SEK': 0.31006599999999906, 'CHE': 0, 'CHW': 0, 'SYP': -12.428308000000015, 'TWD': -1.4130390000000048, 'TJS': 0.09773099999999957, 'TZS': -58.17590800000016, 'THB': -3.763089000000001, 'TOP': -0.04352, 'TTD': -0.21444699999999983, 'TND': -0.2688830000000002, 'TRY': 0.6118410000000001, 'TMT': -0.08446800000000021, 'UGX': -130.37454400000024, 'UAH': -5.186536, 'AED': -0.0886490000000002, 'USN': 0, 'UYI': 0, 'UYU': 4.549678999999998, 'UZS': 1130.9768050000002, 'VUV': -0.9543600000000083, 'VEF': -0.24104400000000048, 'VED': 0, 'VND': -585.6043019999997, 'YER': -5.987554999999986, 'ZMW': 2.1160949999999996, 'ZWL': -8.178009999999972}
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


if __name__ == '__main__':
    currency_code = pd.read_csv('data/currency_code.csv')
    currency_code = currency_code.dropna()
    header = ['Base', 'Date', 'Timestamp']
    symbols = currency_code['Code'].to_list()
    fx_change = build_fx_change_in_year('2019-01-01', '2019-12-31', symbols)
    data = preprocess_and_merge_data(fx_change)
    fx_change_year = data['Fx change']
    score = data['Score']
    plt.plot(score, fx_change_year, 'ro')
    plt.xlabel('Happiness Score')
    plt.ylabel('Fx change in 2019')
    plt.axis([3, 8, -3, 3])
    plt.show()