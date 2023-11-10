import scrapy
from time import sleep


class ColetacolunasSpider(scrapy.Spider):
    name = "coletaColunas"
    
    start_urls = ["https://lista.mercadolivre.com.br/eletronicos-audio-video/acessorios-audio-video/receptores-tv/vivensis/vivensis-vx10_NoIndex_True#applied_filter_id%3DBRAND%26applied_filter_name%3DMarca%26applied_filter_order%3D3%26applied_value_id%3D2571378%26applied_value_name%3DVivensis%26applied_value_order%3D1%26applied_value_results%3D287%26is_custom%3Dfalse"]

    def parse(self, response):
        sleep(1)
        for i in response.xpath('//li[@class="ui-search-layout__item"]'):
            link = i.xpath('.//a[@class="ui-search-item__group__element ui-search-link"]/@href').get()
            titulo = i.xpath('.//h2[@class="ui-search-item__title"]/text()').get()
            
            yield {
                'link':link,
                'titulo':titulo
            }
        
        sleep(0.5)
        next_page = response.xpath('//a[contains (@title, "Seguinte")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)

