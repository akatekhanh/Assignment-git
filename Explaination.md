# Task 1
- I added a Cash class that includes amount and currency_code

# Task 2
- I wrote the get_history_FX_rate in program.py files. It is staticmethod, so any class can use it.
- This function has 2 parameters: 
    + date(str): the date you want to scrape data (i.e: 2019-01-01)
    + currency_code(str): currency code you want to scrape dat (i.e: VND,USD,EUR)
- I used the requests library to scrape data

# Task 3
## Task 3a
- It seems that the website you requested no longer exists or the data is not correct, so I decided to get data from https://www.iban.com/currency-codes. It simply contains a table, I used requests lib to get the page sources and using *lxlm* lib to find the tag elements by xpath. Then convert them to csv and save it as a csv file.
- You can see the function I made in program.get_currency_code
- This function has no input parameters, and it returns a Pandas dataframe

## Task 3b:
- Scrape the ‘Score’ column of the world happiness index from https://en.wikipedia.org/wiki/World_Happiness_Report#2019_report. The same as task 3a, I just use *request* library and *lxlm* to scrape and then save it as a csv file to use later.
- You can see the function I made in program.get_score_world_happiness_index
- This function has no input parameters, and it returns a Pandas dataframe

# Task 4
- Calculate the change of FX rate (in base currency EUR) of a given country between 2 dates. 
- I used the data from 2 & 3a and write the task4() function in task4.py file. 
- Here are the steps that I did:
    + Load the currency code file and preprocess data (dropna values) and get list of symbols
    + Build an FX change table in 2019, return a dictionary as an input of next step
    + I merged currency_code and world_happiness_report as a Pandas dataframe. The dataframe after merging have the form: 'Rank','Score','Country or Region','Code', 'Fx change'
    + I used the Score and Fx_change column to visualize data, and using this data to show examples of linear and polynomial regression (polyfit) between data points
    + I save the image for later analysis
- As you can see, there is a correlation between a countries happiness score (3b) and the change of FX between 2019-01-01 and 2019-12-31. Normally, in countries with low happiness index, FX in 2019 fluctuates very strongly, in contrast to countries with high scores, there is almost no change and tends to increase slightly.

# Task 5
- To value the portfolio, I loaded the currency_code file to get the currencies code, scrape FX rate of those currencies for the day. I then for loop through all the assets in the portfolio, converting them to EUR and calculate sum of my assets.

# Task 6:
- To consolidate the portfolio by unique asset and average cost, I simply for loop through the asset porifolio, merge Cash and Stock by their respective tickers, and sum the tickers once combined.

# Task 7:
- To plot the change in value of our portfolio in EUR throughout 2019. Firstly, I need to scrape FX rate in 2019. For each day of 2019, I will use the function from 5 to value the asset, store those values ​in an array and display them as a column chart.

# Task 8:
- Because of the limited number of api calls, I can only scrape data in 2019 of USD/EUR rates. Using this to display the data, I also masked the weekend data points to check (you can see the graph) and found that, at the weekend data points, there are weeks FX rates Some weeks go up, some weeks go down, some weeks don't seem to change too much.
-> The theory that a reasonable exchange rate is more likely to fall between Friday and Monday because profit taking is not correct

# Task 9
- To calculate PlN, we need to have the FX Rates data in 2019
- We need FX_rates at the time of purchase,It is the first day of 2019 (fx_rates_start)
- It was exercised every weekend of the year, we will take the fx_rates at the end of each week minus fx_rates_start, then multiply by the number of transactions in each week, in our case 100MW/52 (1 year has 52 weeks), then add all these values together
- To calculate PlN: we will take the year-end fx_rates minus the beginning fx_rates and multiply by 100WM. Then subtract the total weekly values.