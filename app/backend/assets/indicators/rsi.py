def calculate_RSI(data, inpPeriodRSI, inpPrice):
    
    #+------------------------------------------------------------------+
    #| Relative Strength Index - Parameters and Buffers                 |
    #+------------------------------------------------------------------+
    extRSIBuffer = []  # RSI Value
    extPosBuffer = []  # RSI Positive Buffer
    extNegBuffer = []  # RSI Negative Buffer

    price = data[f'{inpPrice.capitalize()}']
    price = price.to_list()  # cada elemento double
    rates_total = len(price)
    prev_calculated = 1

    # check for Period Value
    if(inpPeriodRSI < 1):
        extPeriodRSI = 14
        print(f"Incorrect value for variable InpPeriodRSI = {inpPeriodRSI}. RSI will be calculated with value {extPeriodRSI}.")
    else:
        extPeriodRSI = inpPeriodRSI

    #+------------------------------------------------------------------+
    #| Relative Strength Index Calculation                              |
    #+------------------------------------------------------------------+
    def OnCalculate(price, rates_total, prev_calculated = 1):
        # check for min length data
        if(rates_total <= extPeriodRSI):
            for x in range(rates_total):
                extRSIBuffer.append(0)
            return extRSIBuffer

        # preliminary calculations
        pos = prev_calculated - 1

        if(pos <= extPeriodRSI):
            sum_pos = 0
            sum_neg = 0

            # first RSIPeriod values of the indicator are not calculated
            extRSIBuffer.append(0)
            extPosBuffer.append(0)
            extNegBuffer.append(0)

            for i in range(1, extPeriodRSI):
                extRSIBuffer.append(0)
                extPosBuffer.append(0)
                extNegBuffer.append(0)

                diff = price[i] - price[i - 1]

                sum_pos += (diff if diff > 0 else 0)
                sum_neg += (-diff if diff < 0 else 0)

            # calculate first visible value
            extPosBuffer.append(sum_pos / extPeriodRSI)
            extNegBuffer.append(sum_neg / extPeriodRSI)

            if(extNegBuffer[extPeriodRSI] != 0):
                extRSIBuffer.append(100 - (100 / (1 + (extPosBuffer[extPeriodRSI]) / (extNegBuffer[extPeriodRSI]))))
            else:
                if(extPosBuffer[extPeriodRSI] != 0):
                    extRSIBuffer[extPeriodRSI] = extRSIBuffer.append(100)
                else:
                    extRSIBuffer[extPeriodRSI] = extRSIBuffer.append(50)

            # prepare the position value for main calculation
            pos = extPeriodRSI + 1

        # the main loop of calculations
        for i in range(pos, rates_total):
            diff = price[i] - price[i - 1]

            extPosBuffer.append((extPosBuffer[i - 1] * (extPeriodRSI - 1) + (diff if diff > 0 else 0)) / extPeriodRSI)
            extNegBuffer.append((extNegBuffer[i - 1] * (extPeriodRSI - 1) + (-diff if diff < 0 else 0)) / extPeriodRSI)

            if(extNegBuffer[i] != 0):
                extRSIBuffer.append(100 - 100 / (1 + extPosBuffer[i] / extNegBuffer[i]))
            else:
                if(extPosBuffer[i] != 0):
                    extRSIBuffer.append(100)
                else:
                    extRSIBuffer.append(50)

        # OnCalculate done. Return new prev_calculated.
        return extRSIBuffer

    OnCalculate(price=price, rates_total=rates_total)

    #+------------------------------------------------------------------+
    #| Relative Strength Index Values                                   |
    #+------------------------------------------------------------------+
    data[f'RSI{str(extPeriodRSI)}'] = extRSIBuffer

    return data