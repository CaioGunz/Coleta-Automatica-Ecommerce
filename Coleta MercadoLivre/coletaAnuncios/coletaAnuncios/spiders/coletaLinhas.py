import scrapy
from time import sleep

class ColetalinhasSpider(scrapy.Spider):
    name = "coletaLinhas"
    
    start_urls = ["https://lista.mercadolivre.com.br/eletrodomesticos/fornos-fogoes/pecas-acessorios/microondas/elg-mw05sl_BRAND_2489855_NoIndex_True#applied_filter_id%3Dcategory%26applied_filter_name%3DCategorias%26applied_filter_order%3D3%26applied_value_id%3DMLB439510%26applied_value_name%3DPara+Microondas%26applied_value_order%3D2%26applied_value_results%3D37%26is_custom%3Dfalse"]

    def parse(self, response):
        sleep(1)
        for i in response.xpath('//li[@class="ui-search-layout__item"]'):
            titulo = i.xpath('.//h2[@class="ui-search-item__title"]/text()').get()
            link = i.xpath('.//a[@class="ui-search-item__group__element ui-search-link"]/@href').get()
            
            yield {
                'link':link,
                'titulo':titulo
            }
        
        sleep(0.5)
        next_page = response.xpath('//a[contains (@title, "Seguinte")]/@href').get()
        if next_page:
            yield scrapy.Request(url=next_page, callback=self.parse)
