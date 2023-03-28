import pandas as pd
import numpy as np

def setup_123(data, start_date, end_date, multi_trade = False):
    # Dates
    if(len(data) < 2):
        start_date = data.index[0]
        end_date = data.index[0]
    else:
        if (start_date == False):
            start_date = data.index[0]

        if (end_date == False):
            end_date = data.index[-1]

        data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    # Candles
    candles = data
    
    rates_total = len(candles)
    if (rates_total <= 2):
        print('Necessário mais candles para aplicar o modelo')
        candles['buy_sell'] = 0
        candles['price'] = 0
        return candles
    
    candles['buy_sell'] = 0
    candles['price'] = 0
    
    high = candles['High']
    low = candles['Low']
    close = candles['Close']
    open = candles['Open']
    
    buy_sell = []
    price = []
    trigger_candle = []
    max_123 = []
    min_123 = []
    
    prev_calculated = 3
    
    def cal(candles, rates_total, prev_calculated):
        positioned = False
        trigger = False
        
        # 2 primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Trades
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if ((low[i-3] > low[i-2]) and (low[i-2] < low[i-1])):
                    trigger = True
                    trigger_candle.append(i-1)
                    max_123.append(np.max([high[i-3], high[i-2], high[i-1]]))
                    min_123.append(np.min([low[i-3], low[i-2], low[i-1]]))
                if trigger:
                    if (low[i] < min_123[-1]):
                        trigger = False
                        buy_sell.append('NA')
                        trigger_candle.pop()
                        continue
                    if (high[i] > high[trigger_candle[-1]]):
                        trigger = False
                        positioned = True
                        buy_sell.append('B')
                        if (low[i] > high[trigger_candle[-1]]):
                            price.append(open[i])  # GAP
                        else:
                            price.append(high[trigger_candle[-1]] + 0.01)
                        continue
                    else:
                        buy_sell.append('NA')
                else:
                    buy_sell.append('NA')

            # In trade
            if positioned:
                # Sell - STOP
                if (low[i] < min_123[-1]):
                    buy_sell.append('S')
                    price.append(min_123[-1] - 0.01)
                    positioned = False
                    trigger_candle.pop()
                    continue
                # SELL - GAIN
                target = (max_123[-1] - min_123[-1]) * 2 + high[trigger_candle[-1]]
                # Hit target
                if (target < high[i]):
                    buy_sell.append('S')
                    positioned = False
                    trigger_candle.pop()
                    if (target < low[i]):
                        price.append(open[i])  # GAP
                    else:
                        price.append(target)
                    continue
                buy_sell.append('NA')
                continue
                        
        return candles
    
    cal(candles=candles, rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles['buy_sell'] = buy_sell
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles