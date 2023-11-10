import scrapy
from scrapy import Request
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from time import sleep
import pandas as pd

currenctTime = dt.now()
data_dia = str(currenctTime.year) + '-' + str(currenctTime.month) + '-' + str(currenctTime.day)

pd = pd.read_excel('C:/Users/aquario/Desktop/Coleta automatica Ecommerce/bdAnuncios Antenas Externa - FEITO.xlsx')
links = pd['link'].to_list()

lista_valores = []

class ColetaanuncianteSpider(scrapy.Spider):
    name = "coletaAnunciante"
    
    def start_requests(self):
        sleep(0.5)
        for link in links:
            yield Request(link)

        colunms = ['titulo', 'preco', 'estoque', 'linkAnunciante', 'marca', 'sku', 'reputacaoAnunciante', 'linkAnuncio']
        planilha = pd.DataFrame(lista_valores, columns=colunms)
        planilha.to_csv(data_dia + 'coletaAnuncianteMercadoLivre.csv', index=False, sep=';', encoding='utf-8')            

    
    def parse(self, response, **kwargs):
        sleep(0.2)
        titulo =  response.xpath('//h1[@class="ui-pdp-title"]/text()').get()
        preco = response.xpath('//div[@class="ui-pdp-price__second-line"]//span[@class="andes-money-amount__fraction"]/text()').get()
        estoque = response.xpath('//span[@class="ui-pdp-buybox__quantity__available"]/text()').get()
        linkAnunciante= response.xpath('//a[@class="ui-pdp-media__action ui-box-component__action"]/@href').get()
        reputacaoAnunciante = response.xpath('//p[@class="ui-seller-info__status-info__title ui-pdp-seller__status-title"]/text()').get()
        marca = response.xpath('//th[contains(., "Marca")]/following-sibling::td//span[@class="andes-table__column--value"]/text()').get()
        sku = response.xpath('//th[contains(., "Modelo")]/following-sibling::td//span[@class="andes-table__column--value"]/text()').get()
        
        
        lista_valores.append([titulo, preco, estoque, linkAnunciante, marca, sku, reputacaoAnunciante, response.url])     
        print(lista_valores) 

        
process = CrawlerProcess()
process.crawl(ColetaanuncianteSpider)
process.start()
