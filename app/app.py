import pandas as pd
from datetime import datetime

from functions.functions import candles, backtest_trades, backtest_report_calculation, buy_hold, buy_hold_report_calculation
from functions.graphs import graph_balance_report, graph_drawdown_report, graph_trades_return, graph_trades
from functions.setups import frequency, setups_info, setups_description
from functions.tickers import tickers

import streamlit as st

# Streamlit
st.set_page_config(page_title='Meu Setup', layout='wide')

st.subheader("Performance do meu setup")

c1, c2, c3, c4, c5, c6, c7, c8 = st.columns(8)
with c1:
    start_date = st.date_input('Data inicial', value=datetime.strptime('2016-01-01', '%Y-%m-%d'))
with c2:
    end_date = st.date_input('Data Final')
with c3:
    ticker = st.selectbox('Ativo', tickers)
with c4:
    inp_frequency = st.selectbox('Frequência', frequency.keys())
    folder = frequency[inp_frequency]
with c5:
    if (folder == 'wk'):
        inp_setup = st.selectbox('Setup', setups_info.keys())
        setup = str(setups_info[inp_setup] + '_wk')
    elif (folder == 'd'):
        inp_setup = st.selectbox('Setup', setups_info.keys())
        setup = str(setups_info[inp_setup] + '_d')
with c6:
    start_capital = st.number_input(label='Capital Inicial', value=10000, step=1000, format='%d')
with c7:
    trade_cost = st.number_input(label='Custo Operacional', value=4, step=1, format='%d')
with c8:
    risk = st.checkbox(label='Patrimônio Reinvestido', value=False)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.write('Condição:')
    st.write(str(setups_description[setups_info[inp_setup]]['condition']))
with c2:
    st.write('Entrada:')
    st.write(str(setups_description[setups_info[inp_setup]]['entry']))
with c3:
    st.write('Alvo:')
    st.write(str(setups_description[setups_info[inp_setup]]['target']))
with c4:
    st.write('Stop:')
    st.write(str(setups_description[setups_info[inp_setup]]['stop']))

trades = backtest_trades(ticker, start_date=start_date, end_date=end_date, folder=folder, setup=setup, risk=risk, start_capital=start_capital, trade_cost=trade_cost)

backtest_report = backtest_report_calculation(
    ticker, start_date=start_date, end_date=end_date, folder=folder, setup=setup, risk=risk, start_capital=start_capital, trade_cost=trade_cost)

buy_hold = buy_hold(ticker, start_date=start_date, end_date=end_date, folder=folder, start_capital=start_capital, trade_cost=trade_cost)

buy_hold_report = buy_hold_report_calculation(ticker, start_date=start_date, end_date=end_date, folder=folder, start_capital=start_capital, trade_cost=trade_cost)

c1, c2 = st.columns((4,6))
with c1:
    subtab_basic, subtab_all_trades, subtab_win_trades, subtab_loss_trades, subtab_drawndown = st.tabs(['Relatório Básico', 'Total de Trades', 'Trades Ganhadores', 'Trades Perdedores', 'Drawdown'])
    with subtab_basic:
        basic = pd.DataFrame(data=[[f"R${backtest_report['Starting Capital'][0]}", f"R${buy_hold_report['Starting Capital'][0]}"],
                                    [f"R${backtest_report['Total Trade Cost'][0]}", f"R${buy_hold_report['Total Trade Cost'][0]}"],
                                    [f"R${backtest_report['Ending Capital'][0]}", f"R${buy_hold_report['Ending Capital'][0]}"],
                                    [f"{backtest_report['Start Date'][0]}", f"{buy_hold_report['Start Date'][0]}"],
                                    [f"{backtest_report['End Date'][0]}", f"{buy_hold_report['End Date'][0]}"],
                                    [f"R${backtest_report['Net Profit Value'][0]} ({backtest_report['Net Profit %'][0]}%)", f"R${buy_hold_report['Net Profit Value'][0]} ({buy_hold_report['Net Profit %'][0]}%)"],
                                    [f"{backtest_report['Annualized Profit %'][0]}%", f"{buy_hold_report['Annualized Profit %'][0]}%"],
                                    [f"{backtest_report['Annual Volatility %'][0]}%", f"{buy_hold_report['Annual Volatility %'][0]}%"]],
                            index=[['Capital Inicial','Total Trade Cost', 'Capital Final', 'Data Inicial', 'Data Final', 'Lucro', 'Lucro Anualizado', 'Volatilidade Anualizada']], 
                            columns=[str(inp_setup), 'Buy & Hold'])
        st.table(basic)

    with subtab_all_trades:
        all_trades = pd.DataFrame(data=[[f"{backtest_report['Number of Trades'][0]}", f"{buy_hold_report['Number of Trades'][0]}"],
                                        [f"{backtest_report['Active Trade'][0]}", f"{buy_hold_report['Active Trade'][0]}"],
                                        [f"R${backtest_report['Average Return Value'][0]} ({backtest_report['Average Return %'][0]}%)", f"R${buy_hold_report['Average Return Value'][0]} ({buy_hold_report['Average Return %'][0]}%)"],
                                        [f"{backtest_report['Gain/Loss Ratio'][0]}", f"{buy_hold_report['Gain/Loss Ratio'][0]}"],
                                        [f"{backtest_report['Payoff Ratio/Factor'][0]}", f"{buy_hold_report['Payoff Ratio/Factor'][0]}"],
                                        [f"{backtest_report['Mathematical Expectation'][0]}", f"{buy_hold_report['Mathematical Expectation'][0]}"],
                                        [f"{backtest_report['Max Duration'][0]} dias", f"{buy_hold_report['Max Duration'][0]} dias"],
                                        [f"{backtest_report['Average Duration'][0]} dias", f"{buy_hold_report['Average Duration'][0]} dias"],
                                        [f"{backtest_report['Min Duration'][0]} dias", f"{buy_hold_report['Min Duration'][0]} dias"]], 
                                    index=[['Número de trades', 'Trade Ativo', 'Média de retorno', 'Razão Ganho/Perda', 'Payoff', 'Expectativa Matemática', 'Duração Máxima', 'Duração Média', 'Duração Mínima']], 
                                    columns=[str(inp_setup), 'Buy & Hold'])
        st.table(all_trades)

    with subtab_win_trades:
        win_trades = pd.DataFrame(data=[[f"{backtest_report['Number of Gain Trades'][0]}"],
                                        [f"{backtest_report['Win Rate %'][0]}%"],
                                        [f"R${backtest_report['Max Profit Value'][0]} ({backtest_report['Max Profit %'][0]}%)"],
                                        [f"R${backtest_report['Average Profit Value'][0]} ({backtest_report['Average Profit %'][0]}%)"],
                                        [f"R${backtest_report['Min Profit Value'][0]} ({backtest_report['Min Profit %'][0]}%)"],
                                        [f"{backtest_report['Max Win Trade Duration'][0]} dias"],
                                        [f"{backtest_report['Average Win Trade Duration'][0]} dias"],
                                        [f"{backtest_report['Min Win Trade Duration'][0]} dias"],
                                        [f"{backtest_report['Max Consecutive Wins'][0]}"],
                                        [f"{backtest_report['Average Consecutive Wins'][0]}"]],
                                    index=[['Trades Vencedores', 'Taxa de Acerto', 'Lucro Máximo', 'Lucro Médio', 'Lucro Mínimo', 'Duração Máxima', 'Duração Média', 'Duração Mínima', 'Máximo de Ganhos Consecutivos', 'Média de Ganhos Consecutivos']],
                                    columns=[str(inp_setup)])
        st.table(win_trades)

    with subtab_loss_trades:
        loss_trades = pd.DataFrame(data=[[f"{backtest_report['Number of Loss Trades'][0]}"],
                                            [f"{backtest_report['Loss Rate %'][0]}%"],
                                            [f"R${backtest_report['Max Loss Value'][0]} ({backtest_report['Max Loss %'][0]}%)"],
                                            [f"R${backtest_report['Average Loss Value'][0]} ({backtest_report['Average Loss %'][0]}%)"],
                                            [f"R${backtest_report['Min Loss Value'][0]} ({backtest_report['Min Loss %'][0]}%)"],
                                            [f"{backtest_report['Max Loss Trade Duration'][0]} dias"],
                                            [f"{backtest_report['Average Loss Trade Duration'][0]} dias"],
                                            [f"{backtest_report['Min Loss Trade Duration'][0]} dias"],
                                            [f"{backtest_report['Max Consecutive Losses'][0]}"],
                                            [f"{backtest_report['Average Consecutive Losses'][0]}"]],
                                    index=[['Trades Negativos', 'Taxa de Perda', 'Perda Máxima', 'Perda Média', 'Perda Mínima', 'Duração Máxima', 'Duração Média', 'Duração Mínima', 'Máximo de Perdas Consecutivas', 'Média de Perdas Consecutivas']],
                                    columns=[str(inp_setup)])
        st.table(loss_trades)
    
    with subtab_drawndown:
        drawndown = pd.DataFrame(data=[[f"R${backtest_report['Maximum Drawdown Value'][0]}", f"R${buy_hold_report['Maximum Drawdown Value'][0]}"],
                                        [f"{backtest_report['Maximum Drawdown %'][0]}%", f"{buy_hold_report['Maximum Drawdown %'][0]}%"],
                                        [f"{backtest_report['Maximum Drawdown Date'][0]}", f"{buy_hold_report['Maximum Drawdown Date'][0]}"],
                                        [f"{backtest_report['Maximum Drawdown Duration'][0]} dias", f"{buy_hold_report['Maximum Drawdown Duration'][0]} dias"],
                                        [f"{backtest_report['Average Peak Drawdown %'][0]}%", f"{buy_hold_report['Average Peak Drawdown %'][0]}%"],
                                        [f"{backtest_report['Average Drawdown Duration'][0]} dias", f"{buy_hold_report['Average Drawdown Duration'][0]} dias"],
                                        [f"{backtest_report['Recovery Factor'][0]}", f"{buy_hold_report['Recovery Factor'][0]}"]],
                                    index=[['Valor Máximo', 'Porcentagem Máxima', 'Data de Drawdown Máximo', 'Maior Duração', 'Porcentagem Média', 'Duração Média', 'Fator de Recuperação']],
                                    columns=[str(inp_setup), 'Buy & Hold'])
        st.table(drawndown)

    graph_trades_return(trades)
with c2:
    graph_balance_report(buy_hold=buy_hold, trades=trades)
    graph_drawdown_report(buy_hold=buy_hold, trades=trades, avg_dd_peak_pct=backtest_report['Average Peak Drawdown %'][0])

# Candles & Trades
candles = candles(ticker=ticker, start_date=start_date, end_date=end_date, folder=folder)
graph_trades(candles=candles, trades=trades, ticker=ticker)
