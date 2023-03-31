import plotly.graph_objects as go
from datetime import datetime

import streamlit as st

def graph_balance_report(buy_hold, trades):
    balance_buy_hold = buy_hold['balance'].dropna()
    balance_trades = trades['balance'].dropna()
    fig = go.Figure()
    # Buy&Hold Balance
    fig.add_trace(go.Scatter(x=balance_buy_hold.index, y=balance_buy_hold, name='Buy & Hold', line={'color':'lightgrey', "width": 2}))
    # Trades Balance
    fig.add_trace(go.Scatter(x=balance_trades.index, y=balance_trades, name='Setup', line={'color':'green', "width": 3}, fill='tozeroy'))
    fig.update_layout(
        title="Evolução do Patrimônio",
        xaxis={"autorange": True},
        yaxis={"autorange": True, "tickprefix": "R$"},
        yaxis_tickformat = ',.2f',
        hoverlabel={'bgcolor':'grey'},
        width=1100)
    st.plotly_chart(fig)

def graph_drawdown_report(buy_hold, trades, avg_dd_peak_pct):
    # Drawndown Buy&Hold
    wealth_buy_hold = buy_hold[buy_hold['balance'].notna()]
    wealth_buy_hold = wealth_buy_hold['balance']
    previous_peaks_buy_hold = wealth_buy_hold.cummax()
    dd_buy_hold = (wealth_buy_hold - previous_peaks_buy_hold)/previous_peaks_buy_hold
    drawdown_buy_hold = dd_buy_hold * 100
    # Drawndown Trades
    wealth_trades = trades[trades['balance'].notna()]
    wealth_trades = wealth_trades['balance']
    previous_peaks_trades = wealth_trades.cummax()
    dd_trades = (wealth_trades - previous_peaks_trades)/previous_peaks_trades
    drawdown_trades = dd_trades * 100
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=drawdown_buy_hold.index, y=drawdown_buy_hold, name='Buy & Hold', line={'color':'lightgrey', "width": 2}, fill='tozeroy'))
    fig.add_trace(go.Scatter(x=drawdown_trades.index, y=drawdown_trades, name='Setup', line={'color':'#FF6863', "width": 3}, fill='tozeroy'))
    fig.add_hline(-abs(avg_dd_peak_pct), line_dash="dash", line_color="yellow")
    fig.update_layout(
        title='Evolução do Drawdown',
        xaxis={"autorange": True},
        yaxis={"autorange": True, "ticksuffix": "%"},
        yaxis_tickformat = '.2f',
        hoverlabel={'bgcolor':'grey'},
        width=1100)
    st.plotly_chart(fig)

def graph_trades_return(trades):
    profit = trades[trades['buy_sell'] == 'S']
    profit = profit['pct_change']
    fig = go.Figure()
    fig.add_trace(go.Bar(x=profit.index, y=profit, name='Retorno', marker_color='yellow'))
    fig.update_layout(title='Retorno por Trade', 
                      yaxis={"autorange": True, "ticksuffix": "%"}, 
                      yaxis_tickformat = '.2f')
    st.plotly_chart(fig)

def graph_trades(candles, trades, ticker):
    fig = go.Figure(data=[go.Candlestick(x=candles.index,
                                         open=candles['Open'],
                                         high=candles['High'],
                                         low=candles['Low'],
                                         close=candles['Close'],
                                         increasing_line_color= 'white', decreasing_line_color= 'darkred')])
    
    fig.update_layout(
        title=f'Trades de {ticker}',
        xaxis_rangeslider_visible=False,
        width=1800, height=900)
    
    annotations = []
    for i in range(0, len(trades)):
        if (trades['buy_sell'][i] == 'B'):
            annotations.append(go.layout.Annotation({"x": datetime.strptime(str(trades.index[i]), '%Y-%m-%d %H:%M:%S').date(),
                               "y": float(trades['price'][i]),
                               "ax": 0,
                               "ay": 10,
                               "xref": "x",
                               "yref": "y",
                               "xanchor": "left",
                               "arrowhead": 2,
                               "arrowsize": 1.2,
                               "arrowcolor": "rgb(10, 248, 99)"}))
        if (trades['buy_sell'][i] == 'S'):
            annotations.append(go.layout.Annotation({"x": datetime.strptime(str(trades.index[i]), '%Y-%m-%d %H:%M:%S').date(),
                               "y": float(trades['price'][i]),
                               "ax": 0,
                               "ay": -10,
                               "xref": "x",
                               "yref": "y",
                               "xanchor": "left",
                               "arrowhead": 2,
                               "arrowsize": 1.2,
                               "arrowcolor": "rgb(253, 8, 8)"}))
    fig.update_layout(annotations=annotations)
    st.plotly_chart(fig)

def graph_compare_report(backtest_report, axis_x, axis_y):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=backtest_report[axis_x],
                             y=backtest_report[axis_y],
                             mode='markers',
                             text=backtest_report.index,
                             hovertemplate= "<b>%{text}<b><br><br>" + 
                             f'{axis_y}' + ": %{y:.2f}%<br>" + 
                             f'{axis_x}' + ": %{x:.2f}%<br>" + 
                             "Trades: %{marker.color}<extra></extra>", 
                             marker={'color':backtest_report['Number of Trades'],
                                     'colorscale':'plasma','showscale':True}))
    fig.update_layout(title={'text': f"{axis_y}  Vs  {axis_x}"},
                      xaxis={"title":{"text":f"{axis_x}"}, "autorange": True},
                      yaxis={"title":{"text":f"{axis_y}"}, "autorange": True})
    st.plotly_chart(fig)