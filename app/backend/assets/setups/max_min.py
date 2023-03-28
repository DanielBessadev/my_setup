def max_min(data, start_date, end_date, multi_trade = False):
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
    
    candles['buy_sell'] = 0
    candles['price'] = 0
    
    rates_total = len(candles)
    if (rates_total <= 2):
        print('Necessário mais candles para aplicar o modelo')
        candles['buy_sell'] = 0
        candles['price'] = 0
        return candles
    
    high = candles['High']
    low = candles['Low']
    
    buy_sell = []
    price = []
    
    prev_calculated = 2
    
    def cal(candles, rates_total, prev_calculated):
        positioned = False
        
        # 2 primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Trades
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if ((low[i] < low[i-1]) and (low[i] < low[i-2])):
                    positioned = True
                    buy_sell.append('B')
                    price.append(min(low[i-1], low[i-2]) - 0.01)
                    continue
                else:
                    buy_sell.append('NA')

            # In trade
            if positioned:
                # Sell - STOP
                if ((high[i] > high[i-1]) and (high[i] > high[i-2])):
                    buy_sell.append('S')
                    price.append(max(high[i-1], high[i-2]) + 0.01)
                    positioned = False
                    continue
                buy_sell.append('NA')
                continue
                        
        return candles
    
    cal(candles=candles, rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles = candles.assign(buy_sell = buy_sell)
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles