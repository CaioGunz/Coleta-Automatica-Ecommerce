import requests
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from urllib.error import HTTPError

user_agent = ("User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36",
                    "Mozilla/5.0 (compatible; msie 7.0; windows nt 5.0; trident/3.1)",
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_6_8) AppleWebKit/535.2 (KHTML, like Gecko) Chrome/15.0.874.54 Safari/535.2",
                    "Mozilla/5.0 (windows; u; windows nt 6.1) applewebkit/537.1.1 (khtml, like gecko) chrome/37.0.830.0 safari/537.1.1",
                    "Mozilla/5.0 (Macintosh; U; PPC Mac OS X 10_4_11; ja-jp) AppleWebKit/533.16 (KHTML, like Gecko) Version/4.1 Safari/533.16",
                    "Mozilla/5.0 (compatible; msie 9.0; windows nt 5.1; trident/5.0; .net clr 1.5.85128.0)",
                    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.21 (KHTML, like Gecko) Chrome/19.0.1042.0 Safari/535.21",
                    "Mozilla/5.0 (Windows NT 6.2; rv:22.0) Gecko/20130405 Firefox/23.0",
                    "Mozilla/5.0 (windows; u; windows nt 5.2) applewebkit/533.1.1 (khtml, like gecko) chrome/23.0.822.0 safari/533.1.1",
                    "Mozilla/5.0 (windows nt 6.0; win64; x64; rv:7.2) gecko/20100101 firefox/7.2.1",
                    "Mozilla/5.0 (windows; u; windows nt 5.2) applewebkit/531.2.2 (khtml, like gecko) chrome/25.0.899.0 safari/531.2.2")


option = webdriver.ChromeOptions()
option.add_argument(f"user-agent={user_agent}")
servico = Service(ChromeDriverManager().install())

bdAnuncios = pd.read_excel('F:/Pastas CAIO/Coleta automatica Ecommerce/Coleta MercadoLivre/FEITO/anunciosCelularDeMesa - FEITO.xlsx')

driver = webdriver.Chrome(service=servico, options=option)

lista_valores = []
lista_link = []

def proximoLink():
    print('----------------- Inicando Ataque -----------------')
    for index, row in bdAnuncios.iterrows():
        link = row['link']
        categoria = row['Mix']
        lista_link.append(link)
        
        try:
            sleep(1)
            driver.get(link)
            coletaDados(categoria, link)
        except (Exception, HTTPError) as e:
            print('Erro desconhecido ao acessar o link:', str(e))
            sleep(10)
            break
    
        columns = ['titulo', 'preco', 'qtdVendida', 'linkAnunciante', 'reputacaoAnunciante', 'marca', 'categoria', 'sku', 'linkAnuncio']
        planilha = pd.DataFrame(lista_valores, columns=columns)
        planilha.to_csv('coletaAnuncianteCelularDeMesa.csv', sep=';', index=False, encoding='ISO-8859-1')
            
            
def coletaDados(categoria, link):
    try:
        titulo = driver.find_element(By.XPATH, '//h1[@class="ui-pdp-title"]').text
    except:
        titulo = 'null'
    try:
        preco = driver.find_element(By.XPATH, '//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]').text
    except:
        preco = 'null'
    '''
    try:
        estoque = driver.find_element(By.XPATH, '//span[@class="ui-pdp-buybox__quantity__available"]').text
    except:
        estoque = 'null'
    '''
    try:
        linkAnunciante = driver.find_element(By.XPATH, '//a[@class="ui-pdp-media__action ui-box-component__action"]').get_attribute('href')
    except:
        linkAnunciante = 'null'
    try:
        reputacaoAnunciante = driver.find_element(By.XPATH, '//p[@class="ui-seller-info__status-info__title ui-pdp-seller__status-title"]').text
    except:
        reputacaoAnunciante = 'null'
    try:
        marca = driver.find_element(By.XPATH, '//th[contains(., "Marca")]/following-sibling::td//span[@class="andes-table__column--value"]').text
    except:
        marca = 'null'
    try:
        sku = driver.find_element(By.XPATH, '//th[contains(., "Modelo")]/following-sibling::td//span[@class="andes-table__column--value"]').text
    except:
        sku = 'null'
    try:
        qtdVendida = driver.find_element(By.XPATH, '//span[@class="ui-pdp-subtitle"]').text
    except:
        qtdVendida = 'null'
        
    lista_valores.append([titulo, 
                          preco, 
                          qtdVendida,
                          linkAnunciante, 
                          reputacaoAnunciante, 
                          marca, 
                          categoria,
                          sku, 
                          link])
    return proximoLink
    
proximoLink()