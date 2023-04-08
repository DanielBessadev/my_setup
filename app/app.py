import streamlit as st
from PIL import Image

# Streamlit
st.set_page_config(page_title='Meu Setup', layout='wide')

st.title("Meu Setup")

st.write("""
    O acesso de pessoas físicas no mercado financeiro cresce continuamente. A abordagem Quant direciona e auxilia o trader a minimizar o risco nas operações no mercado. O backtest de setups nos diversos ativos é uma ferramenta importante para a tomada de decisões.
    
    Essa ferramenta foi projetada e estruturada em várias páginas que podem ser acessadas usando a barra lateral. Cada uma das páginas aborda uma maneira de analisar o backtest de setups.
        Filtrar o ativo e comparar os diversos setups;
	    Filtrar o setup e comparar os diversos ativos;
	    Analisar a performance do setup e do ativo em maior detalhe.

    Os trades são realizados utilizando todos os dados do ativo e posteriormente filtrados para o período a ser analisado.

    Setups tem entrada única (não é feito multitrading).

    Os trades são feitos somente na ponta da compra.

    Todos os valores dos ativos e estatísticas estão cotadas em Real Brasileiro (BRL).""")

st.subheader("Mercado Financeiro")
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16 = st.columns(16)
c8.image(Image.open('app/images/b3_logo.png'))
c9.image(Image.open('app/images/Yahoo.png'))

st.write("""
    Ativos listados na [**B3**](https://www.b3.com.br/pt_br/).
    
    Dados de mercado baixados da [**API Yahoo! de Finanças**](https://pypi.org/project/yfinance/).

    Maioria dos Setups divulgados pelo trader **Stormer** da [**L&S**](https://ls.com.vc).""")

st.subheader("Ciência de Dados e Engenharia de Dados")
c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16 = st.columns(16)
c6.image(Image.open('app/images/Python.png'))
c7.image(Image.open('app/images/Selenium.png'))
c8.image(Image.open('app/images/Pandas.png'))
c9.image(Image.open('app/images/Numpy.png'))
c10.image(Image.open('app/images/Plotly.png'))
c11.image(Image.open('app/images/Streamlit.png'))

st.write("""
    Lista de Ativos baixados através da biblioteca de automação de navegadores [**Selenium**](https://www.selenium.dev/pt-br/documentation/)

    Transformações e cálculos implementados usando as bibliotecas [**Pandas**](https://pandas.pydata.org/docs/reference/index.html) e [**Numpy**](https://numpy.org/doc/stable/).

    Visualização gráfica realizada com a biblioteca [**Graph Objects (go)**](https://plotly.com/python/graph-objects/) em plotly Python.

    Dashboard escrito em Python usando o framework web [**Streamlit**](https://docs.streamlit.io/library/api-reference).""")

st.write("Isenção de responsabilidade: Não é uma recomendação de compra ou venda de ativos no mercado financeiro.")