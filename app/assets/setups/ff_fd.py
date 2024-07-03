import numpy as np

def ff_fd(data, start_date, end_date, multi_trade = False):
    # Dates
    if(len(data) < 2):
        print(data)
        start_date = data.index[0]
        end_date = data.index[0]
    else:
        if (start_date == False):
            start_date = data.index[0]

        if (end_date == False):
            end_date = data.index[-1]

        data = data[(data.index >= start_date) & (data.index <= end_date)]
    
    # Candles
    candles = data[data['BB20BL'] != np.nan]
    
    rates_total = len(candles)
    if (rates_total <= 0):
        print('Necessário mais candles para aplicar o modelo')
        candles['buy_sell'] = 0
        candles['price'] = 0
        return candles
    
    bb_bl = candles['BB20BL']
    bb_ml = candles['BB20ML']
    open = candles['Open']
    low = candles['Low']
    high = candles['High']
    close = candles['Close']
    
    buy_sell = []
    price = []
    
    prev_calculated = 2
    
    def cal(rates_total, prev_calculated):
        positioned = False
        entry_candle = []
        
        # 2 primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Single trade
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if ((close[i-2] < bb_bl[i-2]) and (close[i-1] > bb_bl[i-1]) and (high[i] > high[i-1])):
                    entry_candle.append(i-1)
                    buy_sell.append('B')
                    positioned = True
                    if (low[i] > high[i-1]):
                        price.append(open[i])  # GAP
                    else:
                        price.append(high[i-1] + 0.01)  # On price
                    continue
                else:
                    buy_sell.append('NA')
                    continue

            # In trade
            if positioned:
                # Sell - STOP
                if (low[i] < low[entry_candle[-1]]):
                    buy_sell.append('S')
                    price.append(low[entry_candle[-1]] - 0.01)
                    positioned = False
                    entry_candle.pop()
                    continue
                # Sell - BB20ML
                if (high[i] >= bb_ml[i-1]):
                    buy_sell.append('S')
                    entry_candle.pop()
                    positioned = False
                    price.append(bb_ml[i-1] + 0.01)   
                    continue
                else:
                    buy_sell.append('NA')
                    continue
                        
        return rates_total
    
    cal(rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles['buy_sell'] = buy_sell
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles