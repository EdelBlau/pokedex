# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['example.com']
    start_urls = ['https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/buscar']

    def parse(self, response):

        for i in range(1, 20):
            link = response.url + str(i)
            yield scrapy.Request(link, self.parse_pagina)

    def parse_pagina(self, response):
        links = response.xpath('//a[@class="re-CardImage-link"]/@href').extract()
        precios = response.xpath('//span[@class="re-Card-price"]/text()').extract()
        # habitaciones = response.xpath('//span[@class="re-Card-wrapperFeatures"]/span/text()')[0].extract()
        # superficies = response.xpath('//span[@class="re-Card-wrapperFeatures"]/span/text()')[1].extract()
        print(links)
        for i in range(0, len(links)):
            item = InmuebleItem()
            item['precio'] = precios[i]
            item['link'] = 'https://www.fotocasa.es' + links[i]
            request = scrapy.Request(item['link'], callback=self.parse_vivienda, meta={'item': item})
            yield request

    def parse_vivienda(self, response):

        item = InmuebleItem()
        item['ciudad'] = response.xpath('//a[@class = "re-Breadcrumb-link"]/text()')[2].get()
        # item['codigoPostal'] = response.xpath( '//p[@class = "fc-DetailDescription"]/text()' ).re_first( r'[0-9]{5}' )
        item['comunidad'] = response.xpath('//a[@class = "re-Breadcrumb-link"]/text()')[0].get()
        item['habitaciones'] = response.xpath('//li[@class = "re-DetailHeader-featuresItem"]/text()')[0].re_first(
            r"([0-9]+) hab")
        item['banos'] = response.xpath('//li[@class = "re-DetailHeader-featuresItem"]/text()')[1].re_first(
            r'([0-9]+) baño')
        item['superficie'] = response.xpath('//li[@class = "re-DetailHeader-featuresItem"]/text()')[2].re_first(
            r'[0-9]+')
        item['precio'] = response.xpath('//span[@class = "re-DetailHeader-price"]/text()').re_first(r'[0-9]+\.[0-9]+')
        item['referencia'] = response.xpath('//span[@class = "re-DetailReference"]/text()').re_first(r'[0-9]+')
        item['particular'] = 'Profesional' if response.xpath(
            '//div[@class = "re-ContactDetail-inmo"]') else 'Particular'
        item['web'] = 'Fotocasa'
        item['link'] = response.url

        yield item
