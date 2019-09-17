# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import PokemonItem


class ExampleSpider(scrapy.Spider):
    name = 'example'
    allowed_domains = ['pokexperto.net']
    start_urls = ['https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/buscar']

    def parse(self, response):
        ult_pokemon = int(response.css('#listapokemon').re_first( r'([0-9]{3}) Pokémon' )) + 1
       # for i in range(1, ult_pokemon):
        for i in range(1, 5):
            link = 'https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/pkmn&pk=' + str(i)
            yield scrapy.Request(link, callback=self.parse_pokemon)


    def parse_pokemon(self, response):
        pokemon = PokemonItem()
        pokemon['id'] = response.css('td.left.pktitle span.amarillo::text').extract_first()
        pokemon['name'] = response.css('td.left.pktitle span.amarillo::text').extract_first()
        pokemon['height'] = response.css('td.left.pktitle span.amarillo::text').extract_first()
        pokemon['weight'] = response.css('td.left.pktitle span.amarillo::text').extract_first()
        pokemon['base_experience'] = response.css('td.left.pktitle span.amarillo::text').extract_first()

        yield pokemon

