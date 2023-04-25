import os
from datetime import datetime, date
import pandas as pd
import numpy as np

def candles(ticker, start_date=False, end_date=False, folder=''):
    ticker = ticker.upper()
    directory=ticker
    parent_dir=f'/app/my_setup/database/stocks_data/{folder}'
    
    if (os.path.isfile(f'{parent_dir}/{directory}/{ticker}_{folder}_quote.csv')):
        candles = pd.read_csv(f'{parent_dir}/{directory}/{ticker}_{folder}_quote.csv', index_col='Date')
    else:
        candles = print(f'No data for {ticker}')
        return candles
    
    # Dates
    if (start_date is False):
        start_date = candles.index[0]
    else:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
        candles.index = pd.to_datetime(candles.index, format='%Y-%m-%d')
        
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d")
        candles = candles.loc[candles.index >= start_date]
        
        # No candles in period
        if (candles.empty):
            print(f'No data for {ticker}')
            return candles

    if (end_date is False):
        end_date = candles.index[-1]
    else:
        candles = candles[candles.index <= end_date]
    
    return candles

def trades_stock(candles, setup, folder=''):
    trades = setup(candles, False, False, False)
    return trades

def backtest_trades(ticker, start_date=False, end_date=False, folder='', setup='', risk=False, start_capital=10000, trade_cost=4):
    ticker = ticker.upper()
    """ directory=ticker
    parent_dir=f'/app/my_setup/database/stocks_data/{folder}' """

    candles = candles(ticker=ticker, start_date=start_date, end_date=end_date, folder=folder)

    trades = trades_stock(candles=candles, setup=setup, folder=folder)

    """ if (os.path.isfile(f'{parent_dir}/{directory}/{ticker}_{setup}.csv')):
        trades = pd.read_csv(f'{parent_dir}/{directory}/{ticker}_{setup}.csv',
                             usecols=['Date','buy_sell','price'],
                             dtype={'buy_sell': 'string', 'price':'float32'},
                             index_col='Date')
    else:
        trades = print(f'No trades for {ticker}')
        return trades """
    
    # No complete trades
    if (len(trades) == 1):
        trades['pct_change'] = 0
        trades['profit'] = np.NaN
        trades['balance'] = start_capital
        print(f'No completed trades for {ticker}')
        return trades
    
    # Dates
    if (start_date is False):
        start_date = trades.index[0]
    else:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
        trades.index = pd.to_datetime(trades.index, format='%Y-%m-%d')
        
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d")
        trades = trades.loc[trades.index >= start_date]
        
        # No trades in period
        if (trades.empty):
            print(f'No trades for {ticker}')
            return trades
        
        # Ignore first sell
        if (trades['buy_sell'][0] == 'S'):
            if (len(trades) == 1):
                trades['pct_change'] = 0
                trades['profit'] = np.NaN
                trades['balance'] = start_capital
                print(f'No completed trades for {ticker}')
                return trades
            else:
                trades = trades[1:]

    if (end_date is False):
        end_date = trades.index[-1]
    else:
        trades = trades[trades.index <= end_date]
    
    # % change
    trades['pct_change'] = trades['price'].pct_change() * 100
    
    # Trades
    idx_sell = trades[trades['buy_sell'] == 'S'].index
    
    # Low Risk - Same value per trade
    if not risk:
        trades.loc[idx_sell, 'profit'] = start_capital * (100 + trades['pct_change']) / 100 - start_capital - (trade_cost*2)
        
        trades['balance'] = np.NaN
        trades['balance'] = trades['profit'].cumsum() + start_capital
        trades.at[trades.index[0], 'balance'] = start_capital
    
    # High Risk - All in trade
    if risk:
        pct_change = trades['pct_change']
        
        trades['profit'] = np.NaN
        profit = trades['profit']
        
        trades['balance'] = np.NaN
        trades.at[trades.index[0], 'balance'] = start_capital
        balance = trades['balance']

        for i in range(0, len(trades[:2])):
            if (i == 0):
                continue
            if (i == 1):
                profit.at[profit.index[i]] = balance.at[balance.index[i-1]] * (100 + pct_change.at[pct_change.index[i]]) / 100 - balance.at[balance.index[i-1]]
                balance.at[balance.index[i]] = balance.at[balance.index[i-1]] + profit.at[profit.index[i]]

        for i in range(3, (len(trades[2:])+1), 2):
            profit.at[profit.index[i]] = balance.at[balance.index[i-2]] * (100 + pct_change.at[pct_change.index[i]]) / 100 - balance.at[balance.index[i-2]]
            balance.at[balance.index[i]] = balance.at[balance.index[i-2]] + profit.at[profit.index[i]]
    
    return trades

def empty_trades_report(ticker, start_capital, trade_cost):
    # Basic Report
    stock = ticker
    start_capital=start_capital
    trade_cost=trade_cost
    total_trade_cost=0
    end_capital=0
    net_profit_value=0
    net_profit_pct=0
    start_date=str('No trades')
    end_date=str('No trades')
    annual_profit_pct=0
    annual_volatility_pct=0
    
    # General Trades
    n_trades=0
    active_trade=str('No')
    avg_ret_value=0
    avg_ret_pct=0
    g_l_ratio=0
    payoff=0
    mat_expec=0
    max_duration=0
    avg_duration=0
    min_duration=0
    
    # Gain Trades
    n_gain=0
    win_rate_pct=0
    max_profit_value=0
    avg_profit_value=0
    min_profit_value=0
    max_profit_pct=0
    avg_profit_pct=0
    min_profit_pct=0
    max_win_duration=0
    avg_win_duration=0
    min_win_duration=0
    max_consec_win=0
    avg_consec_win=0
        
    # Loss Trades
    n_loss=0
    loss_rate_pct=0
    max_loss_value=0
    avg_loss_value=0
    min_loss_value=0
    max_loss_pct=0
    avg_loss_pct=0
    min_loss_pct=0
    max_loss_duration=0
    avg_loss_duration=0
    min_loss_duration=0
    max_consec_loss=0
    avg_consec_loss=0
    
    # Drawdown
    max_dd_value=0
    max_dd_pct=0
    max_dd_date=str('No trades')
    max_dd_duration=0
    avg_dd_peak_pct=0
    avg_dd_duration=0
    dd_recovery_factor=0
    
    backtest_report = pd.DataFrame({
    # Basic Report
    'Stock': str(stock),
    'Starting Capital': float("{:.2f}".format(start_capital)),
    'Trade Cost': float("{:.2f}".format(trade_cost)),
    'Total Trade Cost': float("{:.2f}".format(total_trade_cost)),
    'Ending Capital': float("{:.2f}".format(end_capital)),
    'Net Profit Value': float("{:.2f}".format(net_profit_value)),
    'Net Profit %': float("{:.2f}".format(net_profit_pct)),
    'Start Date': str(start_date),
    'End Date': str(end_date),
    'Annualized Profit %': float("{:.2f}".format(annual_profit_pct)),
    'Annual Volatility %': float("{:.2f}".format(annual_volatility_pct)),
    
    # General Trades
    'Number of Trades': int(n_trades),
    'Active Trade': str(active_trade),
    'Average Return Value': float("{:.2f}".format(avg_ret_value)),
    'Average Return %': float("{:.2f}".format(avg_ret_pct)),
    'Gain/Loss Ratio': float("{:.2f}".format(g_l_ratio)),
    'Payoff Ratio/Factor': float("{:.2f}".format(payoff)),
    'Mathematical Expectation': float("{:.2f}".format(mat_expec)),
    'Max Duration': int(max_duration),
    'Average Duration': int(avg_duration),
    'Min Duration': int(min_duration),
    # avg_stop_value / avg_stop_%
    
    # Gain trades
    'Number of Gain Trades': int(n_gain),
    'Win Rate %': float("{:.2f}".format(win_rate_pct)),
    'Max Profit Value': float("{:.2f}".format(max_profit_value)),
    'Average Profit Value': float("{:.2f}".format(avg_profit_value)),
    'Min Profit Value': float("{:.2f}".format(min_profit_value)),
    'Max Profit %': float("{:.2f}".format(max_profit_pct)),
    'Average Profit %': float("{:.2f}".format(avg_profit_pct)),
    'Min Profit %': float("{:.2f}".format(min_profit_pct)),
    'Max Win Trade Duration': int(max_win_duration),
    'Average Win Trade Duration': int(avg_win_duration),
    'Min Win Trade Duration': int(min_win_duration),
    'Max Consecutive Wins': int(max_consec_win),
    'Average Consecutive Wins': float("{:.2f}".format(avg_consec_win)),
    
    # Loss trades
    'Number of Loss Trades': int(n_loss),
    'Loss Rate %': float("{:.2f}".format(loss_rate_pct)),
    'Max Loss Value': float("{:.2f}".format(max_loss_value)),
    'Average Loss Value': float("{:.2f}".format(avg_loss_value)),
    'Min Loss Value': float("{:.2f}".format(min_loss_value)),
    'Max Loss %': float("{:.2f}".format(max_loss_pct)),
    'Average Loss %': float("{:.2f}".format(avg_loss_pct)),
    'Min Loss %': float("{:.2f}".format(min_loss_pct)),
    'Max Loss Trade Duration': int(max_loss_duration),
    'Average Loss Trade Duration': int(avg_loss_duration),
    'Min Loss Trade Duration': int(min_loss_duration),
    'Max Consecutive Losses': int(max_consec_loss),
    'Average Consecutive Losses': float("{:.2f}".format(avg_consec_loss)),
    
    # Drawdown
    'Maximum Drawdown Value': float("{:.2f}".format(max_dd_value)),
    'Maximum Drawdown %': float("{:.2f}".format(max_dd_pct)),
    'Maximum Drawdown Date': str(max_dd_date),
    'Maximum Drawdown Duration': float("{:.0f}".format(max_dd_duration)),
    'Average Peak Drawdown %': float("{:.2f}".format(avg_dd_peak_pct)),
    'Average Drawdown Duration': float("{:.0f}".format(avg_dd_duration)),
    'Recovery Factor': float("{:.2f}".format(dd_recovery_factor)),
    }, index=range(1))
    
    return backtest_report

def backtest_report_calculation(ticker, start_date, end_date, folder, setup, risk, start_capital, trade_cost):
    trades = backtest_trades(ticker, start_date, end_date, folder, setup, risk, start_capital, trade_cost)

    if (len(trades) <= 1):
        return empty_trades_report(ticker, start_capital, trade_cost)
    
    # Basic Report
    # Stock
    stock = ticker
   
    # Starting Capital
    start_capital = trades['balance'][0]
    
    # Trade Cost - ???????????????????????????????????????????????
    trade_cost = trade_cost

    # Total Trade Cost
    total_trade_cost = trade_cost * len(trades[trades['buy_sell'] == 'S']) * 2
    
    # Ending Capital
    end_capital = trades['balance'].dropna()
    end_capital = end_capital[-1]
    
    # Net Profit Value
    net_profit_value = trades['profit'].sum()
    
    # Net Profit %
    net_profit_pct = net_profit_value * 100 / start_capital
    
    # Start Date
    start_date = datetime.strptime(str(trades.index.min()), '%Y-%m-%d %H:%M:%S').date()
    
    # End Date
    if (trades['buy_sell'][-1] == 'B'):
        end_date = date.today()
    if (trades['buy_sell'][-1] == 'S'):
        end_date = datetime.strptime(str(trades.index.max()), '%Y-%m-%d %H:%M:%S').date()
    
    # Annualized Profit % - Conferir
    # Annual Volatility % - Conferir
    profit = trades[trades['buy_sell'] == 'S']
    profit.index = pd.to_datetime(profit.index, utc=True, errors='coerce')
    
    if(profit.empty):
        annual_profit_pct = 0
        annual_volatility_pct = 0
    else:
        year_profit = profit.groupby(profit.index.year)['pct_change'].sum()
        annual_profit_pct = year_profit.mean()
        
        annual_price = profit.groupby(profit.index.year)['pct_change'].sum()
        annual_mean = annual_price.sum() / len(annual_price)
        annual_deviation = annual_price.apply(lambda x: x - annual_mean)
        annual_deviation_square = annual_deviation ** 2
        annual_variance = annual_deviation_square / len(annual_deviation_square)
        annual_standard_deviation = np.sqrt(annual_variance)
        annual_volatility_pct = annual_standard_deviation.mean()
    
    # General Trades
    # Number of Trades
    n_trades = len(profit)
      
    # Active Trade
    if (trades['buy_sell'][-1] == 'B'):
        active_trade = str('Sim')
    else:
        active_trade = str('Não')
    
    # Average Return Value
    avg_ret_value = trades['profit'].mean()
    
    # Average Return %
    if (profit.empty):
        avg_ret_pct = 0
    else:
        avg_ret_pct = profit['pct_change'].mean()
    
    # Gain/Loss Ratio
    # Payoff Ratio/Factor
    gain = list(filter(lambda i: i >= 0, profit['profit']))
    loss = list(filter(lambda i: i < 0, profit['profit']))
    
    if (len(loss) > 1):
        if (len(gain) > 1):
            g_l_ratio = abs(np.mean(gain)/np.mean(loss))
            payoff = abs(len(gain)/len(loss))
        if (len(gain) == 1):
            g_l_ratio = abs(len(gain)/len(loss))
            payoff = abs(len(gain)/len(loss))
        if (len(gain) == 0):
            g_l_ratio = 0
            payoff = 0
    if (len(loss) == 1):
        if (len(gain) > 1):
            g_l_ratio = np.mean(gain)
            payoff = len(gain)
        if (len(gain) <= 1):
            g_l_ratio = len(gain)
            payoff = len(gain)
    if (len(loss) == 0):
        g_l_ratio = 0
        payoff = 0
    
    # Max Duration
    # Average Duration
    # Min Duration
    duration = []
    dur_end_date=datetime.strptime(str(end_date), '%Y-%m-%d').date()
    
    buy = trades[trades['buy_sell'] == 'B'].index
    buy = pd.to_datetime(buy, utc=True, infer_datetime_format=True)
    
    sell = trades[trades['buy_sell'] == 'S'].index
    sell = pd.to_datetime(sell, utc=True, infer_datetime_format=True)
    
    if (buy.empty):
        max_duration = 0
        avg_duration = 0
        min_duration = 0
    else:
        for i in range(len(buy)+1):
            if i == len(sell):
                duration.append((dur_end_date - buy[-1].date()).days)
                break
            duration.append((sell[i].date() - buy[i].date()).days)

        duration = np.abs(duration)

        max_duration = np.max(duration)
        avg_duration = int(np.mean(duration))
        min_duration = min(duration)
        
    # Gain Trades
    # Number of Gain Trades
    n_gain = len(gain)
    
    # Win Rate %
    if (len(gain) > 0):
        win_rate_pct = (n_gain / n_trades)*100
    else:
        win_rate_pct = 0
     
    # Max Profit Value
    # Average Profit Value
    # Min Profit Value
    if (len(gain) > 0):
        max_profit_value = np.max(gain)
        avg_profit_value = np.mean(gain)
        min_profit_value = np.min(gain)
    else:
        max_profit_value = 0
        avg_profit_value = 0
        min_profit_value = 0
    
    # Max Profit %
    # Average Profit %
    # Min Profit %
    gain_pct = list(filter(lambda i: i >= 0, profit['pct_change']))
    loss_pct = list(filter(lambda i: i < 0, profit['pct_change']))
    
    if (len(gain_pct) > 0):
        max_profit_pct = np.max(gain_pct)
        avg_profit_pct = np.mean(gain_pct)
        min_profit_pct = np.min(gain_pct)
    else:
        max_profit_pct = 0
        avg_profit_pct = 0
        min_profit_pct = 0
    
    # Max Win Trade Duration
    # Average Win Trade Duration
    # Min Win Trade Duration
    profit_duration = []

    buy = trades[trades['buy_sell'] == 'B']
    sell = trades[trades['buy_sell'] == 'S']

    profit_buy = []
    profit_sell = []
    
    for i in range(len(sell)):
        if sell['pct_change'][i] > 0:
            profit_sell.append(sell.index[i])
            profit_buy.append(buy.index[i])

    profit_buy = pd.to_datetime(profit_buy, utc=True, infer_datetime_format=True)
    profit_sell = pd.to_datetime(profit_sell, utc=True, infer_datetime_format=True)
    
    if (len(gain) > 0):
        for i in range(len(profit_buy)+1):   #### testar para len(trade_buy) != len(trade_sell)
            if i == len(profit_sell):
                profit_duration.append((dur_end_date - profit_buy[-1].date()).days)
                break
            profit_duration.append((profit_sell[i].date() - profit_buy[i].date()).days)

        profit_duration = np.abs(profit_duration)

        max_win_duration = np.max(profit_duration)
        avg_win_duration = np.mean(profit_duration)
        min_win_duration = np.min(profit_duration)
    else:
        max_win_duration = 0
        avg_win_duration = 0
        min_win_duration = 0
    
    # Max Consecutive Wins
    # Average Consecutive Winners
    consec_win = []
    win = 0
    
    if (len(gain) > 0):
        for i in range(len(sell)):
            if sell['pct_change'][i] > 0:
                win+=1
                if i == (len(sell)-1):
                    consec_win.append(win)
                continue
            else:
                consec_win.append(win)
                win=0

        max_consec_win = np.max(consec_win)
        avg_consec_win = np.mean(consec_win)
    else:
        max_consec_win = 0
        avg_consec_win = 0
    
    # Loss Trades
    loss = np.positive(loss)
    loss_pct = np.positive(loss_pct)
    
    # Number of Loss Trades
    n_loss = len(loss)
    
    # Loss Rate %
    if (len(loss) > 0):
        loss_rate_pct = (n_loss/n_trades)*100
    else:
        loss_rate_pct = 0
      
    # Max Loss Value
    # Average Loss Value
    # Min Loss Value
    if (len(loss) > 0):
        max_loss_value = np.max(abs(loss))
        avg_loss_value = np.mean(abs(loss))
        min_loss_value = np.min(abs(loss))
    else:
        max_loss_value = 0
        avg_loss_value = 0
        min_loss_value = 0
    
    # Max Loss %
    # Average Loss %
    # Min Loss %
    if (len(loss_pct) > 0):
        max_loss_pct = np.max(abs(loss_pct))
        avg_loss_pct = np.mean(abs(loss_pct))
        min_loss_pct = np.min(abs(loss_pct))
    else:
        max_loss_pct = 0
        avg_loss_pct = 0
        min_loss_pct = 0
    
    # Max Loss Duration
    # Average Loss Duration
    # Min Loss Duration
    loss_duration = []
    
    loss_buy = []
    loss_sell = []
    
    for i in range(len(sell)):
        if sell['pct_change'][i] <= 0:
            loss_sell.append(sell.index[i])
            loss_buy.append(buy.index[i])
    
    loss_buy = pd.to_datetime(loss_buy, utc=True, infer_datetime_format=True)
    loss_sell = pd.to_datetime(loss_sell, utc=True, infer_datetime_format=True)
    
    if (len(loss) > 0):
        for i in range(len(loss_buy)+1):   #### testar para len(trade_buy) != len(trade_sell)
            if i == len(loss_sell):
                loss_duration.append((dur_end_date - loss_buy[-1].date()).days)
                break
            loss_duration.append((loss_sell[i].date() - loss_buy[i].date()).days)

        loss_duration = np.abs(loss_duration)

        max_loss_duration = np.max(loss_duration)
        avg_loss_duration = np.mean(loss_duration)
        min_loss_duration = np.min(loss_duration)
    else:
        max_loss_duration = 0
        avg_loss_duration = 0
        min_loss_duration = 0
    
    # Max Consecutive Losses
    # Average Consecutive Losses
    consec_loss = []
    loss = 0
    
    if (len(gain) > 0):
        for i in range(len(sell)):
            if sell['pct_change'][i] <= 0:
                loss+=1
                if i == (len(sell)-1):
                    consec_loss.append(loss)
                continue
            else:
                consec_loss.append(loss)
                loss=0

        max_consec_loss = np.max(consec_loss)
        avg_consec_loss = np.mean(consec_loss)
    else:
        max_consec_loss = 0
        avg_consec_loss = 0
    
    # Mathematical Expectation
    mat_expec = (win_rate_pct/100 * avg_profit_value) - (loss_rate_pct/100 * avg_loss_value)
    
    # Drawdown
    wealth = trades[trades['balance'].notna()]
    wealth = wealth['balance']  #wealth = (1000 * (1 + pct_change)).cumsum()
    
    previous_peaks = wealth.cummax()
    
    dd=(wealth-previous_peaks)/previous_peaks
    
    # Maximum Drawdown Value
    dd_values = abs(wealth-previous_peaks)
    max_dd_index = abs(dd).idxmax()
    max_dd_value = dd_values.loc[dd_values.index == max_dd_index][0]
    
    # Maximum Drawdown %
    max_dd_pct = abs(dd).max() * 100
    
    # Maximum Drawdown Date
    max_dd_date = datetime.strptime(str(max_dd_index), '%Y-%m-%d %H:%M:%S').date()
    
    # Maximum Drawdown Duration
    max_dd_duration_peak = previous_peaks.value_counts().idxmax()
    
    date_first_peak = previous_peaks.loc[previous_peaks == max_dd_duration_peak].index[0]
    date_first_peak = datetime.strptime(str(date_first_peak), '%Y-%m-%d %H:%M:%S').date()
    
    date_last_peak = previous_peaks.loc[previous_peaks == max_dd_duration_peak].index[-1]
    date_last_peak = datetime.strptime(str(date_last_peak), '%Y-%m-%d %H:%M:%S').date()
    
    for i in range(len(previous_peaks)):
        if ((datetime.strptime(str(previous_peaks.index[i]), '%Y-%m-%d %H:%M:%S').date() - date_last_peak).days > 0):
            date_last_peak = datetime.strptime(str(previous_peaks.index[i]), '%Y-%m-%d %H:%M:%S').date()
            break
        else:
            continue
    
    max_dd_duration = (date_last_peak - date_first_peak).days
    
    # Average Peak Drawdown %
    dds_max_pct = []
    
    for i in range(len(dd)):
        if (i == 0):
            continue
        if (i == (len(dd) - 1)):
            if (dd[i-1] > dd[i]):
                dds_max_pct.append(dd[i])
                break
            break
        if ((i < (len(dd) - 1)) & (dd[i-1] > dd[i]) & (dd[i] < dd[i+1])):
            dds_max_pct.append(dd[i])
            continue
        else:
            continue
    
    if (len(dds_max_pct) > 1):
        avg_dd_peak_pct = abs(np.mean(dds_max_pct)) * 100
    elif (len(dds_max_pct) == 1):
        avg_dd_peak_pct = dds_max_pct[0] * 100
    elif (len(dds_max_pct) == 0):
        avg_dd_peak_pct = 0
    
    # Average Drawdown Duration
    dds_duration = []
    dd_dates_peak = []
    
    for i in range(len(previous_peaks)):
        if (i == 0):
            continue
        if (previous_peaks[i] == previous_peaks[i-1]):
            dd_dates_peak.append(previous_peaks.index[i-1])
            continue
        if (i == (len(previous_peaks) - 2)):
            dd_dates_peak.append(previous_peaks.index[i])
            if (len(dd_dates_peak) > 1):
                dds_duration.append((datetime.strptime(str(dd_dates_peak[-1]), '%Y-%m-%d %H:%M:%S').date() 
                                     - datetime.strptime(str(dd_dates_peak[0]), '%Y-%m-%d %H:%M:%S').date()).days)
            break
        else:
            dd_dates_peak.append(previous_peaks.index[i])
            if (len(dd_dates_peak) > 1):
                dds_duration.append((datetime.strptime(str(dd_dates_peak[-1]), '%Y-%m-%d %H:%M:%S').date() 
                                     - datetime.strptime(str(dd_dates_peak[0]), '%Y-%m-%d %H:%M:%S').date()).days)
            dd_dates_peak = []
    
    if (len(dds_duration) > 1):
        avg_dd_duration = np.mean(dds_duration)
    elif (len(dds_duration) == 1):
        avg_dd_duration = dds_duration[0]
    elif (len(dds_duration) == 0):
        avg_dd_duration = 0
        
    # Recovery Factor
    if (max_dd_value > 0):
        dd_recovery_factor = wealth[-1] / max_dd_value
    else:
        dd_recovery_factor = 0
        
    # Top 5 Worst Drawdown Periods': top5_worst_dd_periods,  # Value / % / Duration / Date
    
    backtest_report = pd.DataFrame({
    # Basic Report
    'Stock': str(stock),
    'Starting Capital': float("{:.2f}".format(start_capital)),
    'Trade Cost': float("{:.2f}".format(trade_cost)),
    'Total Trade Cost': float("{:.2f}".format(total_trade_cost)),
    'Ending Capital': float("{:.2f}".format(end_capital)),
    'Net Profit Value': float("{:.2f}".format(net_profit_value)),
    'Net Profit %': float("{:.2f}".format(net_profit_pct)),
    'Start Date': start_date.strftime("%d/%m/%Y"),
    'End Date': end_date.strftime("%d/%m/%Y"),
    'Annualized Profit %': float("{:.2f}".format(annual_profit_pct)),
    'Annual Volatility %': float("{:.2f}".format(annual_volatility_pct)),
    
    # General Trades
    'Number of Trades': int(n_trades),
    'Active Trade': str(active_trade),
    'Average Return Value': float("{:.2f}".format(avg_ret_value)),
    'Average Return %': float("{:.2f}".format(avg_ret_pct)),
    'Gain/Loss Ratio': float("{:.2f}".format(g_l_ratio)),
    'Payoff Ratio/Factor': float("{:.2f}".format(payoff)),
    'Mathematical Expectation': float("{:.2f}".format(mat_expec)),
    'Max Duration': int(max_duration),
    'Average Duration': int(avg_duration),
    'Min Duration': int(min_duration),
    # avg_stop_value / avg_stop_%
    
    # Gain trades
    'Number of Gain Trades': int(n_gain),
    'Win Rate %': float("{:.2f}".format(win_rate_pct)),
    'Max Profit Value': float("{:.2f}".format(max_profit_value)),
    'Average Profit Value': float("{:.2f}".format(avg_profit_value)),
    'Min Profit Value': float("{:.2f}".format(min_profit_value)),
    'Max Profit %': float("{:.2f}".format(max_profit_pct)),
    'Average Profit %': float("{:.2f}".format(avg_profit_pct)),
    'Min Profit %': float("{:.2f}".format(min_profit_pct)),
    'Max Win Trade Duration': int(max_win_duration),
    'Average Win Trade Duration': int(avg_win_duration),
    'Min Win Trade Duration': int(min_win_duration),
    'Max Consecutive Wins': int(max_consec_win),
    'Average Consecutive Wins': float("{:.2f}".format(avg_consec_win)),
    
    # Loss trades
    'Number of Loss Trades': int(n_loss),
    'Loss Rate %': float("{:.2f}".format(loss_rate_pct)),
    'Max Loss Value': float("{:.2f}".format(max_loss_value)),
    'Average Loss Value': float("{:.2f}".format(avg_loss_value)),
    'Min Loss Value': float("{:.2f}".format(min_loss_value)),
    'Max Loss %': float("{:.2f}".format(max_loss_pct)),
    'Average Loss %': float("{:.2f}".format(avg_loss_pct)),
    'Min Loss %': float("{:.2f}".format(min_loss_pct)),
    'Max Loss Trade Duration': int(max_loss_duration),
    'Average Loss Trade Duration': int(avg_loss_duration),
    'Min Loss Trade Duration': int(min_loss_duration),
    'Max Consecutive Losses': int(max_consec_loss),
    'Average Consecutive Losses': float("{:.2f}".format(avg_consec_loss)),
    
    # Drawdown
    'Maximum Drawdown Value': float("{:.2f}".format(max_dd_value)),
    'Maximum Drawdown %': float("{:.2f}".format(max_dd_pct)),
    'Maximum Drawdown Date': max_dd_date.strftime("%d/%m/%Y"),
    'Maximum Drawdown Duration': float("{:.0f}".format(max_dd_duration)),
    'Average Peak Drawdown %': float("{:.2f}".format(avg_dd_peak_pct)),
    'Average Drawdown Duration': float("{:.0f}".format(avg_dd_duration)),
    'Recovery Factor': float("{:.2f}".format(dd_recovery_factor)),
    }, index=range(1))
    
    return backtest_report

def buy_hold(ticker, start_date=False, end_date=False, folder='', start_capital=10000, trade_cost=4):
    ticker = ticker.upper()
    directory=ticker
    parent_dir=f'/app/my_setup/database/stocks_data/{folder}'

    if (os.path.isfile(f'{parent_dir}/{directory}/{ticker}_{folder}_quote.csv')):
        stock_data = pd.read_csv(f'{parent_dir}/{directory}/{ticker}_{folder}_quote.csv', index_col='Date', engine='python', usecols=['Date','Close'], dtype={'Close':'float32'})
    else:
        stock_data = print(f'No trades for {ticker}')
    
    # Dates
    if (start_date is False):
        start_date = stock_data.index[0]
    else:
        start_date = datetime.strptime(str(start_date), "%Y-%m-%d")
        stock_data.index = pd.to_datetime(stock_data.index, format='%Y-%m-%d')
        
        end_date = datetime.strptime(str(end_date), "%Y-%m-%d")
        stock_data = stock_data.loc[stock_data.index >= start_date]
    
    if (end_date is False):
        end_date = stock_data.index[-1]
    else:
        stock_data = stock_data[stock_data.index <= end_date]
    
    # % change
    stock_data['pct_change'] = stock_data['Close'].pct_change() * 100
    stock_data['pct_change'].fillna(0, inplace=True)

    # Balance
    stock_data['balance'] = np.NaN
    stock_data.at[stock_data.index[0], 'balance'] = start_capital
    
    balance = stock_data['balance']
    pct_change = stock_data['pct_change']
    
    for i in range(0, len(stock_data)):
        if (i == 0):
            continue
        else:
            balance.at[balance.index[i]] = balance.at[balance.index[i-1]] * (100 + pct_change.at[pct_change.index[i]]) / 100
    
    balance.at[balance.index[-1]] = balance.at[balance.index[-1]] - trade_cost

    return stock_data

def buy_hold_report_calculation(ticker, start_date, end_date, folder, start_capital, trade_cost):
    trades = buy_hold(ticker, start_date, end_date, folder, start_capital, trade_cost)

    # Basic Report
    # Stock
    stock = ticker
    
    # Starting Capital
    start_capital = trades['balance'][0]
    
    # Trade Cost - ???????????????????????????????????????????????
    trade_cost = trade_cost

    # Total Trade Cost
    total_trade_cost = trade_cost
    
    # Ending Capital
    end_capital = trades['balance'][-1]
    
    # Net Profit Value
    net_profit_value = trades['balance'][-1] - start_capital
    
    # Net Profit %
    net_profit_pct = net_profit_value * 100 / start_capital
    
    # Start Date
    start_date = datetime.strptime(str(trades.index.min()), '%Y-%m-%d %H:%M:%S').date()
    
    # End Date
    end_date = datetime.strptime(str(trades.index.max()), '%Y-%m-%d %H:%M:%S').date()
    
    # Annualized Profit % - Conferir
    trades.index = pd.to_datetime(trades.index, utc=True, errors='coerce')
    
    year_profit = trades.groupby(trades.index.year)['pct_change'].sum()
    annual_profit_pct = year_profit.mean()
    
    # Annual Volatility % - Conferir
    annual_mean = year_profit.sum() / len(year_profit)
    annual_deviation = year_profit.apply(lambda x: x - annual_mean)
    annual_deviation_square = annual_deviation ** 2
    annual_variance = annual_deviation_square / len(annual_deviation_square)
    annual_standard_deviation = np.sqrt(annual_variance)
    annual_volatility_pct = annual_standard_deviation.mean()
    
    # General Trades
    # Number of Trades
    n_trades = 1
      
    # Active Trade
    active_trade = str('Sim')
    
    # Average Return Value
    avg_ret_value = net_profit_value
    
    # Average Return %
    avg_ret_pct = net_profit_pct
    
    # Gain/Loss Ratio
    # Payoff Ratio/Factor
    if (trades['balance'][-1] >= 0):
        gain = 1
        loss = 0
    if (trades['balance'][-1] < 0):
        gain = 0
        loss = 1
    
    if (loss == 1):
        g_l_ratio = gain / loss
        payoff = gain / loss
    if (loss == 0):
        g_l_ratio = 0
        payoff = 0
    
    # Max Duration
    buy = trades.index[0]
    sell = trades.index[-1]
    
    duration = (sell - buy).days
    
    max_duration = duration
    
    # Average Duration
    avg_duration = duration
    
    # Min Duration
    min_duration = duration
    
    # Gain Trades
    # Number of Gain Trades
    n_gain = 0
    
    # Win Rate %
    win_rate_pct = 0
    
    # Max Profit Value
    profit_value = 0
    profit_pct = 0
    profit_duration = 0
    
    max_profit_value = profit_value
    
    # Average Profit Value
    avg_profit_value = profit_value
    
    # Min Profit Value
    min_profit_value = profit_value
    
    # Max Profit %
    max_profit_pct = profit_pct
    
    # Average Profit %
    avg_profit_pct = profit_pct
    
    # Min Profit %
    min_profit_pct = profit_pct
    
    # Max Win Trade Duration
    max_win_duration = profit_duration
    
    # Average Win Trade Duration
    avg_win_duration = profit_duration
    
    # Min Win Trade Duration
    min_win_duration = profit_duration
    
    # Max Consecutive Wins
    max_consec_win = n_gain
    
    # Average Consecutive Winners
    avg_consec_win = n_gain
    
    # Loss Trades
    # Number of Loss Trades
    n_loss = 0
    
    # Loss Rate %
    loss_rate_pct = 0
    
    # Max Loss Value
    loss_value = 0
    loss_pct = 0
    loss_duration = 0
    
    max_loss_value = loss_value
    
    # Average Loss Value
    avg_loss_value = loss_value
    
    # Min Loss Value
    min_loss_value = loss_value
    
    # Max Loss %
    max_loss_pct = loss_pct
    
    # Average Loss %
    avg_loss_pct = loss_pct
    
    # Min Loss %
    min_loss_pct = loss_pct
    
    # Max Loss Duration
    max_loss_duration = loss_duration
    
    # Average Loss Duration
    avg_loss_duration = loss_duration
    
    # Min Loss Duration
    min_loss_duration = loss_duration
    
    # Max Consecutive Losses': max_consec_loss
    max_consec_loss = n_loss
    
    # Average Consecutive Losses
    avg_consec_loss = n_loss

    # Mathematical Expectation
    mat_expec = (win_rate_pct/100 * avg_profit_value) - (loss_rate_pct/100 * avg_loss_value)
    
    # Drawdown
    wealth = trades[trades['balance'].notna()]
    wealth = wealth['balance']  #wealth = (1000 * (1 + pct_change)).cumsum()
    
    previous_peaks = wealth.cummax()
    
    dd=(wealth-previous_peaks)/previous_peaks  #drawdown=(wealth_index-previous_peaks)/previous_peaks
    
    # Maximum Drawdown Value
    dd_values = abs(wealth-previous_peaks)
    max_dd_index = abs(dd).idxmax()
    max_dd_value = dd_values.loc[dd_values.index == max_dd_index][0]
    
    # Maximum Drawdown %
    max_dd_pct = abs(dd).max() * 100
    
    # Maximum Drawdown Date
    max_dd_date = max_dd_index.date()
    
    # Maximum Drawdown Duration
    max_dd_duration_peak = previous_peaks.value_counts().idxmax()
    date_first_peak = previous_peaks.loc[previous_peaks == max_dd_duration_peak].index[0]
    date_last_peak = previous_peaks.loc[previous_peaks == max_dd_duration_peak].index[-1]
    
    for i in range(len(previous_peaks)):
        if ((previous_peaks.index[i] - date_last_peak).days > 0):
            date_last_peak = previous_peaks.index[i]
            break
        else:
            continue
    
    max_dd_duration = (date_last_peak - date_first_peak).days
    
    # Average Peak Drawdown %
    dds_max_pct = []
    for i in range(len(dd)):
        if (i == 0):
            continue
        if (i == (len(dd) - 1)):
            if (dd[i-1] > dd[i]):
                dds_max_pct.append(dd[i])
                break
            break
        if ((i < (len(dd) - 1)) & (dd[i-1] > dd[i]) & (dd[i] < dd[i+1])):
            dds_max_pct.append(dd[i])
            continue
        else:
            continue
            
    avg_dd_peak_pct = abs(np.mean(dds_max_pct)) * 100
    
    # Average Drawdown Duration
    dds_duration = []
    dd_dates_peak = []
    for i in range(len(previous_peaks)):
        if (i == 0):
            continue
        if (previous_peaks[i] == previous_peaks[i-1]):
            dd_dates_peak.append(previous_peaks.index[i-1])
            continue
        if (i == (len(previous_peaks) - 2)):
            dd_dates_peak.append(previous_peaks.index[i])
            if (len(dd_dates_peak) > 1):
                dds_duration.append((dd_dates_peak[-1] - dd_dates_peak[0]).days)
            break
        else:
            dd_dates_peak.append(previous_peaks.index[i])
            if (len(dd_dates_peak) > 1):
                dds_duration.append((dd_dates_peak[-1] - dd_dates_peak[0]).days)
            dd_dates_peak = []
    
    avg_dd_duration = np.mean(dds_duration)
    
    # Recovery Factor
    dd_recovery_factor = wealth[-1] / max_dd_value
      
    # Top 5 Worst Drawdown Periods': top5_worst_dd_periods,  # Value / % / Duration / Date
    
    buy_hold_report = pd.DataFrame({
    # Basic Report
    'Stock': str(stock),
    'Starting Capital': float("{:.2f}".format(start_capital)),
    'Trade Cost': float("{:.2f}".format(trade_cost)),
    'Total Trade Cost': float("{:.2f}".format(total_trade_cost)),
    'Ending Capital': float("{:.2f}".format(end_capital)),
    'Net Profit Value': float("{:.2f}".format(net_profit_value)),
    'Net Profit %': float("{:.2f}".format(net_profit_pct)),
    'Start Date': start_date.strftime("%d/%m/%Y"),
    'End Date': end_date.strftime("%d/%m/%Y"),
    'Annualized Profit %': float("{:.2f}".format(annual_profit_pct)),
    'Annual Volatility %': float("{:.2f}".format(annual_volatility_pct)),
    
    # General Trades
    'Number of Trades': int(n_trades),
    'Active Trade': str(active_trade),
    'Average Return Value': float("{:.2f}".format(avg_ret_value)),
    'Average Return %': float("{:.2f}".format(avg_ret_pct)),
    'Gain/Loss Ratio': float("{:.2f}".format(g_l_ratio)),
    'Payoff Ratio/Factor': float("{:.2f}".format(payoff)),
    'Mathematical Expectation': float("{:.2f}".format(mat_expec)),
    'Max Duration': int(max_duration),
    'Average Duration': int(avg_duration),
    'Min Duration': int(min_duration),
    # avg_stop_value / avg_stop_%
    
    # Gain trades
    'Number of Gain Trades': int(n_gain),
    'Win Rate %': float("{:.2f}".format(win_rate_pct)),
    'Max Profit Value': float("{:.2f}".format(max_profit_value)),
    'Average Profit Value': float("{:.2f}".format(avg_profit_value)),
    'Min Profit Value': float("{:.2f}".format(min_profit_value)),
    'Max Profit %': float("{:.2f}".format(max_profit_pct)),
    'Average Profit %': float("{:.2f}".format(avg_profit_pct)),
    'Min Profit %': float("{:.2f}".format(min_profit_pct)),
    'Max Win Trade Duration': int(max_win_duration),
    'Average Win Trade Duration': int(avg_win_duration),
    'Min Win Trade Duration': int(min_win_duration),
    'Max Consecutive Wins': int(max_consec_win),
    'Average Consecutive Wins': float("{:.2f}".format(avg_consec_win)),
    
    # Loss trades
    'Number of Loss Trades': int(n_loss),
    'Loss Rate %': float("{:.2f}".format(loss_rate_pct)),
    'Max Loss Value': float("{:.2f}".format(max_loss_value)),
    'Average Loss Value': float("{:.2f}".format(avg_loss_value)),
    'Min Loss Value': float("{:.2f}".format(min_loss_value)),
    'Max Loss %': float("{:.2f}".format(max_loss_pct)),
    'Average Loss %': float("{:.2f}".format(avg_loss_pct)),
    'Min Loss %': float("{:.2f}".format(min_loss_pct)),
    'Max Loss Trade Duration': int(max_loss_duration),
    'Average Loss Trade Duration': int(avg_loss_duration),
    'Min Loss Trade Duration': int(min_loss_duration),
    'Max Consecutive Losses': int(max_consec_loss),
    'Average Consecutive Losses': float("{:.2f}".format(avg_consec_loss)),
    
    # Drawdown
    'Maximum Drawdown Value': float("{:.2f}".format(max_dd_value)),
    'Maximum Drawdown %': float("{:.2f}".format(max_dd_pct)),
    'Maximum Drawdown Date': max_dd_date.strftime("%d/%m/%Y"),
    'Maximum Drawdown Duration': float("{:.0f}".format(max_dd_duration)),
    'Average Peak Drawdown %': float("{:.2f}".format(avg_dd_peak_pct)),
    'Average Drawdown Duration': float("{:.0f}".format(avg_dd_duration)),
    'Recovery Factor': float("{:.2f}".format(dd_recovery_factor)),
    }, index=range(1))
    
    return buy_hold_report

def all_stocks_setup_report(tickers, start_date=False, end_date=False, folder='', setup='', risk=False, start_capital=10000, trade_cost=4):
    for ticker in tickers:
        ticker = ticker.upper()
        ticker_backtest_report = backtest_report_calculation(ticker, start_date=start_date, end_date=end_date, folder=folder, setup=setup, risk=risk, start_capital=start_capital, trade_cost=trade_cost)
        
        if (ticker == tickers[0]):
            backtest_report = ticker_backtest_report
        else:
            backtest_report = pd.concat([ticker_backtest_report, backtest_report])
    
    backtest_report.set_index('Stock', inplace=True)
    return backtest_report

def all_reports_by_stock(ticker, start_date=False, end_date=False, folder='', setups='', risk=False, start_capital=10000, trade_cost=4):
    
    setup_reports = buy_hold_report_calculation(ticker=ticker, start_date=start_date, end_date=end_date, folder=folder, start_capital=start_capital, trade_cost=trade_cost)
    setup_reports.set_index('Stock', inplace=True)
    
    for setup in setups:
        ticker = ticker.upper()
        report = backtest_report_calculation(ticker=ticker, start_date=start_date, end_date=end_date, folder=folder, setup=setup, risk=risk, start_capital=start_capital, trade_cost=trade_cost)
        report.index = [setup]
        setup_reports = pd.concat([setup_reports, report])
        
    return setup_reports
