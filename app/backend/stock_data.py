import yfinance as yf
import pandas as pd
import os
from shutil import rmtree
from tqdm import tqdm

def stocks_list():
    df = pd.read_csv('../database/b3_stocks.csv', usecols=['Código'], dtype={'Código': 'string'})
    tickers = df['Código'].sort_values().to_list()
    return tickers

def download_stocks_quotes(freq=''):
    tickers = stocks_list()

    for ticker in tqdm(tickers):
        # Diretório
        directory=ticker
        parent_dir=f'C:/Users/danie/Documents/Projeto/database/stocks_data/{freq}'
        path = os.path.join(parent_dir, directory)
        rmtree(path=path, ignore_errors=True)
        os.mkdir(path)
        
        if (freq == 'wk'):
            interval='1wk'
        elif (freq == 'd'):
            interval='1d'

        # Download
        quote = yf.download(ticker+'.SA', period='max', interval=interval, show_errors=False, progress=False)[['Open', 'High', 'Low', 'Close', 'Volume']]
        
        #if (freq == 'd'):
        #    quote.index.strftime('%Y/%m/%d')

        # Save
        quote.to_csv(f'{parent_dir}/{directory}/{ticker}_{freq}_quote.csv')