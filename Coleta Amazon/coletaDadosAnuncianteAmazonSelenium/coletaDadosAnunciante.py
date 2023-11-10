import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime as dt
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#* Pega a data do dia em que o código foi rodado no formato (DD-MM-YYYY)
currenctTime = dt.now()
data_dia = str(currenctTime.year) + '-' + str(currenctTime.month) + '-' + str(currenctTime.day)

servico = Service(ChromeDriverManager().install())

driver = webdriver.Chrome(service=servico)

bdAnunciante = pd.read_csv('C:/Users/aquario/Desktop/Coleta automatica Ecommerce/2023-10-9coletaAnuncianteAmazon.csv', sep=';')

lista_valores = []
linkAnunciante = []

def pegalink():

    for index, row in bdAnunciante.iterrows():
        link = row['linkVendedor']
        linkAnunciante.append(link)
        
        try:
            sleep(0.2)
            print("----------------------Iniciando o Ataque em: " + link)
            driver.get(link)
            
            coletaDados()
            
            '''
            nomeComercial = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[2]/span[2]').text
            cnpj = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[3]/span[2]').text
            telefone = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[4]/span[2]').text
            rua = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[6]/span').text
            referencia = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[7]/span').text
            cidade = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[8]/span').text
            estado = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[9]/span').text
            cep = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[10]/span').text
            pais = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[11]/span').text
            '''
            
        except Exception as e:
            print("Ataque mal sucedido/loja amazon")
    
    colunms = ['nomeComercial', 'CNPJ', 'telefone', 'rua', 'cidade', 'estado', 'cep', ' linkAnunciante']
    planilha = pd.DataFrame(lista_valores, columns=colunms)
    planilha.to_csv(data_dia + 'dadosAnuncianteColetados.csv', index=False, sep=';', encoding='iso-8859-1')
    print('Ataque finalizado com sucesso!!!')

def coletaDados():  
    
    '''
    try:
        nomeComercial = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[2]/span[2]').text
    except:
        nomeComercial = ''
    try:
        cnpj = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[3]/span[2]').text
    except:
        cnpj = ''
    try:
        telefone = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[4]/span[2]').text
    except:
        telefone = ''
    try:
        rua = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[6]/span').text
    except:
        rua = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[5]/span').text
    try:
        cidade = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[8]/span').text
    except:
        cidade = ''
    try:
        estado = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[9]/span').text
    except:
        estado = ''
    try:
        cep = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[10]/span').text
    except:
        cep = ''    
    try:
        pais = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[11]/span').text
    except:
        pais = ''
    '''
    
    try:
        nomeComercial = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[2]/span[2]').text
    except:
        nomeComercial = ''

    try:
        cnpj = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[3]/span[2]').text
    except:
        cnpj = ''

    try:
        telefone = driver.find_element(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div[4]/span[2]').text
    except:
        telefone = ''
    try:
        elements = driver.find_elements(By.XPATH, '//*[@id="page-section-detail-seller-info"]/div/div/div/div/span')
        
        if len(elements) <= 5:
            rua = elements[5].text or elements[6] or elements[7]
        else:
            rua = ''
        
        if len(elements) >= 8:
            cidade = elements[7].text
        else:
            cidade = ''
        
        if len(elements) >= 9:
            estado = elements[8].text
        else:
            estado = ''
        
        if len(elements) >= 10:
            cep = elements[9].text
        else:
            cep = ''
        
    except Exception as e:
        print("Erro na coleta - REINICIANDO!!")

    
        
    sleep(0.2)
    lista_valores.append([nomeComercial, cnpj, telefone, rua, cidade, estado, cep, linkAnunciante[-1]])
    sleep(0.5)
    return pegalink


pegalink()
