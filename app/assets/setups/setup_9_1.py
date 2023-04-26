from assets.indicators.ma import calculate_MA

def setup_9_1(data, start_date, end_date, multi_trade = False):
    # EMA9
    data = calculate_MA(data=data, inpCandle='Close', InpMAMethod='EMA', InpMAPeriod=9)

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
    candles = data[data['EMA9'] > 0]
    if (len(candles.index) <= 1):
        print('Necessário mais candles para aplicar o modelo')
        candles['buy_sell'] = 0
        candles['price'] = 0
        return candles
    
    rates_total = len(candles)
    
    ema9 = candles['EMA9']
    open = candles['Open']
    high = candles['High']
    low = candles['Low']
    close = candles['Close']
    
    if (rates_total <= 2):
        print('Necessário mais candles para aplicar o modelo')
        candles.drop([0,1])
        return candles
    
    buy_sell = []
    price = []
    entry_trigger_candle = []
    exit_trigger_candle = []
    
    prev_calculated = 2
    
    def cal(candles, rates_total, prev_calculated):
        positioned = False
        entry_trigger = False
        exit_trigger = False
        
        # 2 primeiros candles
        for i in range(0, prev_calculated):
            buy_sell.append('NA')
        
        # Trades
        for i in range(prev_calculated, rates_total):
            # No trade done
            if not positioned:
                # BUY
                if ((ema9[i-3]>=ema9[i-2]) and (ema9[i-2]<ema9[i-1])):
                    entry_trigger = True
                    entry_trigger_candle.append(i-1)
                if entry_trigger:
                    # Trade válido enquanto a ema9 continua ascendente
                    if (high[i] > high[entry_trigger_candle[-1]]):
                        entry_trigger = False
                        positioned = True
                        buy_sell.append('B')
                        if (low[i] > high[entry_trigger_candle[-1]]):
                            price.append(open[i])  # GAP
                        else:
                            price.append(high[entry_trigger_candle[-1]] + 0.01)
                        continue
                    else:
                        buy_sell.append('NA')
                else:
                    buy_sell.append('NA')

            # In trade
            if positioned:
                # Sell - STOP
                if (low[i] < low[entry_trigger_candle[-1]]):
                    buy_sell.append('S')
                    price.append(low[entry_trigger_candle[-1]] - 0.01)
                    positioned = False
                    entry_trigger_candle.pop()
                    continue
                # Sell - GAIN
                if ((ema9[i-3]<ema9[i-2]) and (ema9[i-2]>ema9[i-1])):
                    exit_trigger = True
                    exit_trigger_candle.append(i-1)
                if exit_trigger:
                    # Saída válida enquanto a ema9 continua descendente
                    if ((low[i] < low[exit_trigger_candle[-1]]) and (ema9[i-1]>ema9[i])):
                        exit_trigger = False
                        positioned = False
                        buy_sell.append('S')
                        price.append(low[exit_trigger_candle[-1]] - 0.01)
                        exit_trigger_candle.pop()
                        continue
                    # Exit Not Triggered
                    if not (ema9[i-1]>ema9[i]):
                        exit_trigger = False
                        buy_sell.append('NA')
                        exit_trigger_candle.pop()
                        continue
                    else:
                        buy_sell.append('NA')
                else:
                    buy_sell.append('NA')
                        
        return candles
    
    cal(candles=candles, rates_total=rates_total, prev_calculated=prev_calculated)
    
    candles = candles.assign(buy_sell = buy_sell)
    candles = candles[candles['buy_sell'] != 'NA']
    
    candles = candles.assign(price = price)
    
    return candles