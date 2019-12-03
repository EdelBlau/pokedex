# -*- coding: utf-8 -*-
import scrapy


class PokedexSpider(scrapy.Spider):
    name = 'pokedex'
    allowed_domains = ['pokemon.com']
    start_urls = ['http://pokemon.com/']

    def parse(self, response):
        pass
