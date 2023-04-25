import pandas as pd
import numpy as np

def calculate_BB(data, inpCandle, InpBandsPeriod, InpBandsDeviations):
    
    #+------------------------------------------------------------------+
    #| Inputs - Bollinger Bands                                         |
    #+------------------------------------------------------------------+   
    if(InpBandsPeriod < 2):
        ExtBandsPeriod = 20
    else:
        ExtBandsPeriod = InpBandsPeriod
   
    if(InpBandsDeviations == 0):
        ExtBandsDeviations = 2
    else:
        ExtBandsDeviations = InpBandsDeviations
    
    #+------------------------------------------------------------------+
    #| Bollinger Bands Calculation                                      |
    #+------------------------------------------------------------------+
    price = data[f'{inpCandle.capitalize()}']
    
    period = ExtBandsPeriod
    deviation = ExtBandsDeviations
    
    rates_total = len(price)
    
    # Check for min length data
    if(rates_total < period):
        ExtMLBuffer, ExtTLBuffer, ExtBLBuffer = [], [], []
        for x in range(rates_total):
            ExtMLBuffer.append(np.nan)
            ExtTLBuffer.append(np.nan)
            ExtBLBuffer.append(np.nan)
        data[f'BB{str(period)}TL'] = ExtTLBuffer
        data[f'BB{str(period)}ML'] = ExtMLBuffer
        data[f'BB{str(period)}BL'] = ExtBLBuffer
        return data
    
    if (rates_total >= period):
        ExtMLBuffer = pd.Series((price.rolling(period).mean()), name=f'BB{str(period)}ML')
        ExtStdDevBuffer = price.rolling(period).std(ddof=0)

        ExtTLBuffer = pd.Series((ExtMLBuffer + deviation * ExtStdDevBuffer), name=f'BB{str(period)}TL')
        ExtBLBuffer = pd.Series((ExtMLBuffer - deviation * ExtStdDevBuffer), name=f'BB{str(period)}BL')
        
        data = pd.concat([data, ExtTLBuffer, ExtMLBuffer, ExtBLBuffer], axis=1)
    
    return data