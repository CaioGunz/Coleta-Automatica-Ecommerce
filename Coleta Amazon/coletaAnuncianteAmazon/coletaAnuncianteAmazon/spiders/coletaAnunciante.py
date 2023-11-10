import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
import numpy as np
import pandas as pd
from datetime import datetime as dt
from time import sleep

currenctTime = dt.now()
data_dia = str(currenctTime.year) + '-' + str(currenctTime.month) + '-' + str(currenctTime.day)

#* Faz a leitura do arquivo csv contendo os links de cada produto
bdAnuncios = pd.read_csv('C:/Users/aquario/Desktop/Coleta automatica Ecommerce/2023-10-5anunciosColetadosAmazon.csv', sep=';')
links = bdAnuncios['link'].to_list()


#*Inicia a lista vazia
lista_valores = []


class ColetaanuncianteSpider(scrapy.Spider):
    name = "coletaAnunciante"

    def start_requests(self):
    
        #*Pega o link da planilha com os anuncios e 
        for link in links:
            sleep(0.5)
            yield Request(link)

    def parse(self, response, **kwargs):
        
        '''Parte em que é feito a coleta dos dados a partir do XPATH da página, pode acrescentar ou diminuir conforme necessario. Se for
        modificado é preciso alterar o LISTA_VALORES no APPEND e o COLUMS para que os dados sejam salvos'''
        titulo = response.xpath('//span[contains(@id, "productTitle")]/text()').get()
        preco = response.xpath('//div[@class="a-section a-spacing-micro"]//span[@class="a-price-whole"]/text()').get()
        linkVendedor = response.xpath('//span[@class="a-size-small offer-display-feature-text-message"]//a[contains (@id, "sellerProfileTriggerId")]/@href').get()
        vendedorSemLink = response.xpath('//div[contains (@id,"merchantInfoFeature_feature_div")]//span[@class="a-size-small offer-display-feature-text-message"]/text()').get()
        nomeVendedor = response.xpath('//span[@class="a-size-small offer-display-feature-text-message"]//a[contains (@id, "sellerProfileTriggerId")]/text()').get()
        marca = response.xpath('//tr[@class="a-spacing-small po-brand"]//span[@class="a-size-base po-break-word"]/text()').get()
        sku = response.xpath('//tr[@class="a-spacing-small po-model_name"]//span[@class="a-size-base po-break-word"]/text()').get()
        
        #*Pega o link do vendedor e se não houver link traz a loja oficial da amazon, pois é a unica que não possui link
        if linkVendedor != None:
            linkVendedorCompleto = 'https://www.amazon.com.br' + linkVendedor
        elif vendedorSemLink:
            linkVendedorCompleto = vendedorSemLink
        else:
            linkVendedorCompleto = ' '
        
        #*Verifica se é a loja oficial da amazon, se for preenche como sim, caso contrario como não
        if vendedorSemLink:
            lojaOficial = 'sim'
        else:
            lojaOficial = 'Nao' 
            
        #*Coloca os dados coletados em uma DataFrame temporário para depois ser gerado o arquivo de Output  
        lista_valores.append([titulo, preco, linkVendedorCompleto, nomeVendedor, lojaOficial, marca, sku, response.url])
        
        '''Salva os dados em um Dataframe que vai sair em um Output como csv nesse caso ou xlsx se for modificado para Excel seguindo
        o que o colums definiu, se for necessario acrecentar ou remover é preciso alterar o COLUMS e o LISTA_VALORES no APPEND'''
        colums = ['titulo', 'preco', 'linkVendedor', 'nomeVendedor', 'lojaOficial', 'marca', 'sku', 'linkAnuncio']
        planilha = pd.DataFrame(lista_valores, columns=colums)
        planilha.to_csv(data_dia + 'coletaAnuncianteAmazon.csv', index=False, sep=';', encoding='utf-8')
          
#*Inicia o Scrapy sem precisar utilizar o CMD(Prompt) 
process = CrawlerProcess()
process.crawl(ColetaanuncianteSpider)
process.start()


