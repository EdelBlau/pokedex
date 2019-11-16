# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import scrapy
from scrapy import Request
from tutorial.items import PokemonItem

class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

    def parse(self, response):
        pokemon = PokemonItem()
        pokemon['id'] = response.css('div.pokedex-pokemon-pagination-title div span::text').re_first('[0-9]{3}')
        pokemon['name'] = response.css('div.pokedex-pokemon-pagination-title div::text').extract_first().strip()
        pokemon['description'] = response.css('div.version-descriptions p.active::text').extract_first().strip()
        pokemon['evolution'] = response.css('section.pokedex-pokemon-evolution li span::text').re('[0-9]{3}')
        pokemon['type'] = response.css('div.pokedex-pokemon-attributes div.dtm-type ul')[0].css("li a::text").extract()
        pokemon['height'] = response.css('div.pokemon-ability-info ul li')[0].css("span.attribute-value::text").re_first('\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")
        pokemon['weight'] = response.css('div.pokemon-ability-info ul li')[1].css("span.attribute-value::text").re_first('\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")

        # next pokemon
        url = response.css("div.pokedex-pokemon-pagination a.next::attr(href)").extract_first()
        yield Request(urljoin("https://www.pokemon.com", url), callback=self.parse)

        yield pokemon