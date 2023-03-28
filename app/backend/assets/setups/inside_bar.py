def inside_bar(data, start_date, end_date, multi_trade = False):
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
    
    prev_calculated = 2
    
    def cal(candles, rates_total, prev_calculated):
        positioned = False
        inside_bar_trigger = False
        
        inside_bar_candle = []
        
        # Primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Trades
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if ((low[i-1] >= low[i-2]) and (high[i-1] <= high[i-2])):
                    inside_bar_trigger = True
                    inside_bar_candle.append(i-1)
                if inside_bar_trigger:
                    if (low[i] < low[inside_bar_candle[-1]]) or (low[inside_bar_candle[-1]] == high[inside_bar_candle[-1]]):
                        inside_bar_trigger = False
                        buy_sell.append('NA')
                        inside_bar_candle.pop()
                        continue
                    if (high[i] > high[inside_bar_candle[-1]]) and (high[i] > close[inside_bar_candle[-1]]):
                        inside_bar_trigger = False
                        positioned = True
                        buy_sell.append('B')
                        if (low[i] > high[inside_bar_candle[-1]]):
                            price.append(open[i])
                        else:
                            price.append(high[inside_bar_candle[-1]] + 0.01)
                        continue
                    else:
                        buy_sell.append('NA')
                else:
                    buy_sell.append('NA')

            # In trade
            if positioned:
                # Sell - STOP
                if (low[i] < low[inside_bar_candle[-1]]):
                    buy_sell.append('S')
                    price.append(low[inside_bar_candle[-1]] - 0.01)
                    positioned = False
                    inside_bar_candle.pop()
                    continue
                # SELL - GAIN
                target = (high[inside_bar_candle[-1]] - low[inside_bar_candle[-1]]) * 2 + high[inside_bar_candle[-1]]
                # Hit target
                if ((target > low[i]) and (target < high[i])):
                    buy_sell.append('S')
                    positioned = False
                    inside_bar_candle.pop()
                    price.append(target)
                    continue
                # Low higher than target
                if (target < low[i]):
                    buy_sell.append('S')
                    positioned = False
                    inside_bar_candle.pop()
                    price.append(low[i])
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