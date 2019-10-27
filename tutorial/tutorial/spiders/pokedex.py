# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from tutorial.items import PokemonItem

class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['https://www.pokemon.com/es/pokedex/bulbasaur']

    def parse(self, response):
        pokemon = PokemonItem()
        pokemon['name'] = response.css('div.pokedex-pokemon-pagination-title div::text').extract_first().strip()
        pokemon['id'] = response.css('div.pokedex-pokemon-pagination-title div span::text').re_first('[0-9]{3}')
        pokemon['evolution'] = response.css('section.pokedex-pokemon-evolution li span::text').re('[0-9]{3}')
        pokemon['type'] = response.css('div.pokedex-pokemon-attributes div.dtm-type ul')[0].css("li a::text").extract()

        #next pokemon
        url = response.css("div.pokedex-pokemon-pagination a.next::attr(href)").extract_first()
        yield Request(urljoin("https://www.pokemon.com", url), callback=self.parse)

        yield pokemon