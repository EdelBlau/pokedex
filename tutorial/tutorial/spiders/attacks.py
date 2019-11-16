# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import PokemonAttacksItem, AttackItem


class AttackSpider(scrapy.Spider):
    name = 'attacks'
    allowed_domains = ['pokexperto.net']
    start_urls = ['https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/buscar']

    def parse(self, response):
        ult_pokemon = int(response.css('#listapokemon').re_first( r'([0-9]{3}) Pokémon' )) + 1
        for i in range(1, ult_pokemon):
        #for i in range(1, 5):
            link = 'https://www.pokexperto.net/index2.php?seccion=nds/nationaldex/movimientos_pokemon&pk=' + str(i)
            yield scrapy.Request(link, callback=self.parse_pokemon)

    def parse_pokemon(self, response):
        pokemon = PokemonAttacksItem()
        pokemon['pokemon_id'] = response.css('td.left.pktitle span.amarillo::text').extract_first()
        pokemon["attack_list"] = []
        attacks_html = response.xpath('//tr[@class="check3 bazul"]')
        for attack_html in attacks_html:
            attack = AttackItem()
            attack["type"] = attack_html.css('td img::attr(src)').re_first("tipos/(.*).png").capitalize()
            attack["name"] = attack_html.css('a.nav6c::text').extract_first()
            pokemon["attack_list"].append(attack)

        yield pokemon

