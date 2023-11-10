import scrapy
import pandas as pd
from scrapy.crawler import CrawlerProcess
from datetime import datetime as dt
from time import sleep


currenctTime = dt.now()
data_dia = str(currenctTime.year) + '-' + str(currenctTime.month) + '-' + str(currenctTime.day)
lista_valores = []

class ColetaanunciosamazonSpider(scrapy.Spider):
    name = "coletaAnunciosAmazon"

    start_urls = ["https://www.amazon.com.br/s?rh=n%3A16209062011&fs=true&ref=lp_16209062011_sar"]

    def parse(self, response):
        for i in response.xpath('//div[@class="sg-col-4-of-24 sg-col-4-of-12 s-result-item s-asin sg-col-4-of-16 sg-col s-widget-spacing-small sg-col-4-of-20"]'):
            titulo = i.xpath('.//span[@class="a-size-base-plus a-color-base a-text-normal"]/text()').get()
            link = i.xpath('.//a[@class="a-link-normal s-no-outline"]/@href').get()
            
            
            linkCompleto = 'https://www.amazon.com.br' + link
            
            lista_valores.append([linkCompleto, titulo])
            
        columns = ['link', 'titulo']
        planilha = pd.DataFrame(lista_valores, columns= columns)
        planilha.to_csv(data_dia + 'anunciosColetadosAmazon.csv', sep=';', index=False, encoding='utf-8')

        next_page = response.xpath('//a[@class="s-pagination-item s-pagination-next s-pagination-button s-pagination-separator"]/@href').get()
        if next_page:
            sleep(2)
            yield scrapy.Request(url='https://www.amazon.com.br' + next_page, callback=self.parse)

process = CrawlerProcess()
process.crawl(ColetaanunciosamazonSpider)
process.start()