tickers_pd = pd.read_csv('/app/my_setup/database/b3_stocks.csv')
tickers = tickers_pd['Código'].sort_values().to_list()