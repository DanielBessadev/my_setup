import numpy as np

def calculate_MA(data, inpCandle, InpMAMethod, InpMAPeriod):
    
    #+------------------------------------------------------------------+
    #| Simple Moving Average                                            |
    #+------------------------------------------------------------------+
    def CalculateSMA(rates_total, prev_calculated, price):
        #--- first calculation
        if(prev_calculated == InpMAPeriod - 1):
            ExtLineBuffer.append(np.sum(price[:InpMAPeriod]) / InpMAPeriod)
        #--- main loop
        for i in range(prev_calculated+1, rates_total):
            ExtLineBuffer.append(np.sum(price[i-InpMAPeriod+1:i+1]) / InpMAPeriod)
        return ExtLineBuffer
    
    #+------------------------------------------------------------------+
    #| Exponential Moving Average                                       |
    #+------------------------------------------------------------------+
    def CalculateEMA(rates_total, prev_calculated, price):
        smoothFactor = 2 / (1 + InpMAPeriod)
        #--- first calculation
        if(prev_calculated == InpMAPeriod - 1):
            ExtLineBuffer.append(np.sum(price[:InpMAPeriod]) / InpMAPeriod)
        #--- main loop
        for i in range(prev_calculated+1, rates_total):
            ExtLineBuffer.append(price[i] * smoothFactor + ExtLineBuffer[i-1] * (1 - smoothFactor))
        return ExtLineBuffer
    
    #+------------------------------------------------------------------+
    #| Parameters and Buffers - Moving Average                          |
    #+------------------------------------------------------------------+
    price = data[f'{inpCandle.capitalize()}']
    price = price.to_list()  # cada elemento double
    
    rates_total = len(price)
    prev_calculated = 0
    begin = 0
    
    period = InpMAPeriod
    
    ExtLineBuffer = []
    
    #+------------------------------------------------------------------+
    #| Moving Average Calculation                                       |
    #+------------------------------------------------------------------+
    # check for min length data
    if(rates_total < InpMAPeriod):
        for x in range(rates_total):
            ExtLineBuffer.append(0)
        return ExtLineBuffer

    # preliminary calculations
    if(prev_calculated < InpMAPeriod):
        # first MA values of the indicator are not calculated
        ExtLineBuffer.append(0)
        for i in range(begin+1, InpMAPeriod - 1):
            ExtLineBuffer.append(0)

        # prepare the position value for main calculation
        prev_calculated = InpMAPeriod - 1
    
    method = InpMAMethod
    if method == "EMA":  # Exponential Moving Average
        CalculateEMA(rates_total=rates_total, prev_calculated=prev_calculated, price=price)
    elif method == 'SMA':  # Simple Moving Average
        CalculateSMA(rates_total=rates_total, prev_calculated=prev_calculated, price=price)
    
    #+------------------------------------------------------------------+
    #| Moving Average Values                                            |
    #+------------------------------------------------------------------+
    data[f'{method}{period}'] = ExtLineBuffer
    
    return data