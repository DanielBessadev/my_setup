from b3_stocks import b3_stocks
from stock_data import download_stocks_quotes, stocks_list
from setups import trades_stocks

from assets.setups.ff_fd import ff_fd
from assets.setups.inside_bar import inside_bar
from assets.setups.max_min import max_min
from assets.setups.pfr import pfr
from assets.setups.rsi_2 import rsi_2
from assets.setups.setup_123 import setup_123
from assets.setups.setup_9_1 import setup_9_1

print('DOWNLOADING THE LIST OF STOCKS FROM B3')
b3_stocks()
print('DOWNLOAD COMPLETED')

print('PREPARING THE LIST TO DOWNLOAD QUOTES')
tickers = stocks_list()
print('LIST DEFINED')

print('DOWNLOADING WEEKLY QUOTES')
download_stocks_quotes(freq='wk')
print('WEEKLY QUOTES DOWNLOAD COMPLETED')

print('DOWNLOADING DAILY QUOTES')
download_stocks_quotes(freq='d')
print('DAILY QUOTES DOWNLOAD COMPLETED')

folders = ['d', 'wk']
setups = [ff_fd, inside_bar, max_min, pfr, rsi_2, setup_123, setup_9_1]

for folder in folders:
    for setup in setups:
        print(f'APPLYING {setup.__name__} SETUP {folder}')
        trades_stocks(tickers, setup=setup, folder=folder)

print('EVERYTHING READY')