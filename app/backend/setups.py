import pandas as pd
from tqdm import tqdm

def trades_stocks(tickers, setup, folder=''):
    for ticker in tqdm(tickers):
        # Data
        directory=ticker
        parent_dir=f'C:/Users/danie/Documents/Projeto/database/stocks_data/{folder}'
        
        quote = pd.read_csv(f'{parent_dir}/{directory}/{ticker}_{folder}_quote.csv', index_col='Date', engine='python')
        
        # Check Data
        if (len(quote) <= 1):
            continue
        
        # Trades
        trades = setup(quote, False, False, False)
        trades.to_csv(f'{parent_dir}/{directory}/{ticker}_{setup.__name__}_{folder}.csv')
