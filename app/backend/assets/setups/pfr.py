def pfr(data, start_date, end_date, multi_trade = False):
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
    
    high = candles['High']
    low = candles['Low']
    close = candles['Close']
    open = candles['Open']
    
    buy_sell = []
    price = []
    pfr_candle = []
    
    prev_calculated = 2
    
    def cal(candles, rates_total, prev_calculated):
        positioned = False
        pfr_trigger = False
        
        # 2 primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Trades
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if (((low[i] < low[i-1]) and (low[i] < low[i-2])) and (close[i] > close[i-1])):
                    pfr_trigger = True
                    pfr_candle.append(i)
                if pfr_trigger:
                    if (low[i] < low[pfr_candle[-1]]):
                        pfr_trigger = False
                        buy_sell.append('NA')
                        pfr_candle.pop()
                        continue
                    if (high[i] > high[pfr_candle[-1]]) and (high[i] > close[pfr_candle[-1]]):
                        pfr_trigger = False
                        positioned = True
                        buy_sell.append('B')
                        if (low[i] > high[pfr_candle[-1]]):
                            price.append(open[i])  # GAP
                        else:
                            price.append(high[pfr_candle[-1]] + 0.01)
                        continue
                    else:
                        buy_sell.append('NA')
                else:
                    buy_sell.append('NA')

            # In trade
            if positioned:
                # Sell - STOP
                if (low[i] < low[pfr_candle[-1]]):
                    buy_sell.append('S')
                    price.append(low[pfr_candle[-1]] - 0.01)
                    positioned = False
                    pfr_candle.pop()
                    continue
                # SELL - GAIN
                target = (high[pfr_candle[-1]] - low[pfr_candle[-1]]) * 2 + high[pfr_candle[-1]]
                
                if (target < high[i]):
                    buy_sell.append('S')
                    positioned = False
                    pfr_candle.pop()
                    if (target < low[i]):
                        price.append(open[i])  # Up GAP - Low higher than target
                    else:
                        price.append(target)  # Hit target
                    continue
                buy_sell.append('NA')
                continue
                        
        return candles
    
    cal(candles=candles, rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles = candles.assign(buy_sell = buy_sell)
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles