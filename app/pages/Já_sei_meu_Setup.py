from datetime import datetime, date
from dateutil.relativedelta import relativedelta

from functions.functions import all_stocks_setup_report
from functions.graphs import graph_compare_report
from functions.report import report_columns
from functions.setups import frequency, setups_info
from functions.tickers import tickers

import streamlit as st

# Streamlit
st.set_page_config(page_title='Meu Setup', layout='wide')

st.subheader("Performance do meu setup em todos os ativos")

c1, c2, c3, c4, c5, c6, c7 = st.columns(7)
with c1:
    today = date.today()
    five_years = today + relativedelta(years = -5)
    start_date = st.date_input('Data inicial', value=datetime.strptime(str(five_years), '%Y-%m-%d'))
with c2:
    end_date = st.date_input('Data Final')
with c3:
    inp_frequency = st.selectbox('Frequência', frequency.keys())
    folder = frequency[inp_frequency]
with c4:
    if (folder == 'wk'):
        inp_setup = st.selectbox('Setup', setups_info.keys())
        setup = str(setups_info[inp_setup] + '_wk')
    elif (folder == 'd'):
        inp_setup = st.selectbox('Setup', setups_info.keys())
        setup = str(setups_info[inp_setup] + '_d')
with c5:
    start_capital = st.number_input(label='Capital Inicial', value=10000, step=1000, format='%d')
with c6:
    trade_cost = st.number_input(label='Custo Operacional', value=6, step=1, format='%d')
with c7:
    risk = st.checkbox(label='Patrimônio Reinvestido', value=False)

all_stocks_setup_report = all_stocks_setup_report(tickers, start_date=start_date, end_date=end_date, folder=folder, setup=setup, risk=risk, start_capital=start_capital, trade_cost=trade_cost)

see_data = st.expander('Clique aqui para ver todos os dados 👉')
with see_data:
    st.dataframe(all_stocks_setup_report.style.format({
        # Basic Report
        'Stock': "{:}",
        'Starting Capital': "{:.2f}",
        'Trade Cost': "{:.2f}",
        'Total Trade Cost': "{:.2f}",
        'Ending Capital': "{:.2f}",
        'Net Profit Value': "{:.2f}",
        'Net Profit %': "{:.2f}",
        'Start Date': "{:}",
        'End Date': "{:}",
        'Annualized Profit %': "{:.2f}",
        'Annual Volatility %': "{:.2f}",
        # General Trades
        'Number of Trades': "{:.0f}",
        'Active Trade': "{:}",
        'Average Return Value': "{:.2f}",
        'Average Return %': "{:.2f}",
        'Gain/Loss Ratio': "{:.2f}",
        'Payoff Ratio/Factor': "{:.2f}",
        'Mathematical Expectation': "{:.2f}",
        'Max Duration': "{:.0f}",
        'Average Duration': "{:.0f}",
        'Min Duration': "{:.0f}",
        # avg_stop_value / avg_stop_%
        # Gain trades
        'Number of Gain Trades': "{:.0f}",
        'Win Rate %': "{:.2f}",
        'Max Profit Value': "{:.2f}",
        'Average Profit Value': "{:.2f}",
        'Min Profit Value': "{:.2f}",
        'Max Profit %': "{:.2f}",
        'Average Profit %': "{:.2f}",
        'Min Profit %': "{:.2f}",
        'Max Win Trade Duration': "{:.0f}",
        'Average Win Trade Duration': "{:.0f}",
        'Min Win Trade Duration': "{:.0f}",
        'Max Consecutive Wins': "{:.0f}",
        'Average Consecutive Wins': "{:.2f}",
        # Loss trades
        'Number of Loss Trades': "{:.0f}",
        'Loss Rate %': "{:.2f}",
        'Max Loss Value': "{:.2f}",
        'Average Loss Value': "{:.2f}",
        'Min Loss Value': "{:.2f}",
        'Max Loss %': "{:.2f}",
        'Average Loss %': "{:.2f}",
        'Min Loss %': "{:.2f}",
        'Max Loss Trade Duration': "{:.0f}",
        'Average Loss Trade Duration': "{:.0f}",
        'Min Loss Trade Duration': "{:.0f}",
        'Max Consecutive Losses': "{:.0f}",
        'Average Consecutive Losses': "{:.2f}",
        # Drawdown
        'Maximum Drawdown Value': "{:.2f}",
        'Maximum Drawdown %': "{:.2f}",
        'Maximum Drawdown Date': "{:}",
        'Maximum Drawdown Duration': "{:.2f}",
        'Average Peak Drawdown %': "{:.2f}",
        'Average Drawdown Duration': "{:.2f}",
        'Recovery Factor': "{:.2f}"}
    ))

axis = all_stocks_setup_report.columns.to_list()

c1, c2 = st.columns((2, 8))
with c1:
    st.write("Escolha as estatísticas que serão comparadas")
    inp_axis_y = st.selectbox('Eixo Y', report_columns.values(), index=6)
    axis_y = str(list(report_columns.keys())[list(report_columns.values()).index(inp_axis_y)])
    inp_axis_x = st.selectbox('Eixo X', report_columns.values(), index=48)
    axis_x = str(list(report_columns.keys())[list(report_columns.values()).index(inp_axis_x)])
with c2:
    graph_compare_report(all_stocks_setup_report, axis_x, axis_y)
