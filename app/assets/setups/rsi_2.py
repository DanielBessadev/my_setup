def rsi_2(data, start_date, end_date, multi_trade = False):
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
    candles = data[data['RSI2'] > 0]
    candles = candles[candles['RSI2'] < 100]
    
    rates_total = len(candles)
    if (rates_total <= 0):
        print('Necessário mais candles para aplicar o modelo')
        candles['buy_sell'] = 0
        candles['price'] = 0
        return candles
    
    rsi = candles['RSI2']
    high = candles['High']
    close = candles['Close']
    
    buy_sell = []
    price = []
    
    prev_calculated = 1
    
    def cal(candles, rates_total, prev_calculated = 1):
        pos = prev_calculated - 1
        
        positioned = False
        entry_candle = []
        
        # Single trade
        for i in range(pos, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if (rsi[i] < 25):
                    entry_candle.append(i)
                    buy_sell.append('B')
                    price.append(close[i])
                    positioned = True
                    continue
                else:
                    buy_sell.append('NA')
                    continue

            # In trade
            if positioned:
                # Sell - Last 2 High
                if ((high[i] > high[i-1]) and (high[i] > high[i-2])):
                    buy_sell.append('S')
                    price.append(max(high[i-1], high[i-2]) + 0.01)
                    entry_candle.pop()
                    positioned = False
                    continue
                # Sell - 7 days
                if (entry_candle[-1] + 7) == i:
                    buy_sell.append('S')
                    price.append(close[i])
                    entry_candle.pop()
                    positioned = False
                    continue
                
                else:
                    buy_sell.append('NA')
                    continue
                        
        return candles
    
    cal(candles=candles, rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles['buy_sell'] = buy_sell
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles