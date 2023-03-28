import pandas as pd
import os
from time import sleep, strftime

from selenium.webdriver import Edge
from selenium.webdriver.common.by import By

def download_b3_stocks():
    driver = Edge(executable_path='C:\Program Files (x86)\edgedriver_win64/msedgedriver.exe')
    url = 'https://sistemaswebb3-listados.b3.com.br/indexPage/stocks'
    driver.get(url)
    sleep(2)
    
    driver.find_element(By.XPATH, "/html/body/app-root/app-stocks-index/div/form/div[6]/div/div/div[1]/div[2]/p/a").click()
    sleep(10)
    
    driver.close()
    
    database = pd.read_csv(f'C:/Users/danie/Downloads/AcoesIndices_{strftime("%Y")}-{strftime("%m")}-{strftime("%d")}.csv',  
                           encoding='ISO-8859-1', 
                           engine='python',
                           sep=';',
                           skiprows=3,
                           index_col=False,
                           names=['Empresa', 'Tipo Ação', 'Código', 'Índice'])
    
    os.remove(f'C:/Users/danie/Downloads/AcoesIndices_{strftime("%Y")}-{strftime("%m")}-{strftime("%d")}.csv')
    
    return database

def b3_stocks():
    # Ativos B3
    stocks = download_b3_stocks()

    # FIIs - 'CI' / BDRs - 'DRN'
    fiis_bdrs = stocks.loc[lambda stocks: (stocks['Tipo Ação'] == 'CI') | (stocks['Tipo Ação'] == 'DRN')]

    # DataFrame para Ações
    stocks_b3 = stocks.copy()

    # Retirar FIIs e BDRs
    stocks_b3.drop(fiis_bdrs.index, inplace=True)

    # Salvar arquivo
    stocks_b3.to_csv('../database/b3_stocks.csv')