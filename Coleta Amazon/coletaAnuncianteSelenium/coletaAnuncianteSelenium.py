import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime as dt
from time import sleep

currenctTime = dt.now()
data_dia = str(currenctTime.year) + '-' + str(currenctTime.month) + '-' + str(currenctTime.day)

servico = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=servico)

bdAnuncio = pd.read_csv('C:/Users/aquario/Desktop/Coleta automatica Ecommerce/2023-10-2anunciosColetadosAmazon.csv', sep=';')

lista_valores = []
linkAnuncio = []

def pegaLink():
    for index, row in bdAnuncio.iterrows():
        link = row['link']
        linkAnuncio.append([link])
        
        try:
            sleep(0.5)
            print('Iniciando o Ataque em: ' + link)
            driver.get(link)
            
            coletaDados()
    
        except Exception as e:
            print('Ataque Fracassado :(')
    
    colunms = ['titulo', 'preco', 'linkVendedor', 'nomeVendedor', ' linkAnunciante'] # 'categoria', 'marca', 'sku' acrescentar esses args depois
    planilha = pd.DataFrame(lista_valores, columns=colunms)
    planilha.to_csv(data_dia + 'dadosAnuncianteColetados.csv', index=False, sep=';', encoding='iso-8859-1')
    print('Ataque finalizado com sucesso!!!')

#*Verificar por que não esta puxando os dados
def coletaDados(categoria, marca, sku):
    titulo = driver.find_element(By.XPATH, '//span[contains (@id, "productTitle")]"').text
    preco = driver.find_element(By.XPATH, '//*[@id="corePrice_feature_div"]/div/span[1]/span[2]/span[2]').text
    linkVendedor = driver.find_element(By.XPATH, '//*[@id="sellerProfileTriggerId"]').get_attribute('href')
    nomeVendedor = driver.find_element(By.XPATH, '//*[@id="sellerProfileTriggerId"]').text
    vendedorSemLink = driver.find_element(By.XPATH, '//*[@id="merchantInfoFeature_feature_div"]/div[2]/div/span').text

    if linkVendedor != None:
        linkVendedorCompleto = 'https:www.amazon.com.br' + linkVendedor
    elif vendedorSemLink:
        linkVendedorCompleto = vendedorSemLink
    else:
        linkVendedorCompleto = ''
        
    if vendedorSemLink:
        lojaOficial = 'Sim'
    else:
        lojaOficial = 'Nao'
    
    sleep(0.25)
    lista_valores.append([titulo, preco, linkVendedorCompleto, nomeVendedor, lojaOficial, categoria, marca, sku, linkAnuncio[-1]])
    sleep(0.5)
    return pegaLink

pegaLink()