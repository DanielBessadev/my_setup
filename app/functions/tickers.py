import pandas as pd

tickers_pd = pd.read_csv('database/b3_stocks.csv')
tickers = tickers_pd['Código'].sort_values().to_list()