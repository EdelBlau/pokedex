# -*- coding: utf-8 -*-
import scrapy


class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

    def parse(self, response):
        self.log('----------INFORMACIÓN DE BULBASAUR------------')
        self.log('ID: {}'.format(response.css('div.pokedex-pokemon-pagination-title div span::text').re_first('[0-9]{3}')))
        self.log('name: {}'.format(response.css('div.pokedex-pokemon-pagination-title div::text').extract_first().strip()))
        self.log('description: {}'.format(response.css('div.version-descriptions p.active::text').extract_first().strip()))
        self.log('evolution: {}'.format(response.css('section.pokedex-pokemon-evolution li span::text').re('[0-9]{3}')))
        self.log('type: {}'.format(response.css('div.pokedex-pokemon-attributes div.dtm-type ul')[0].css("li a::text").extract()))
        self.log('height: {}'.format(response.css('div.pokemon-ability-info ul li')[0].css("span.attribute-value::text").re_first('\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")))
        self.log('weight: {}'.format(response.css('div.pokemon-ability-info ul li')[1].css("span.attribute-value::text").re_first('\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")))
        self.log('-----------------------------------------------')