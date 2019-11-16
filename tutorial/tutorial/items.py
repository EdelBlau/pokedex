# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class PokemonItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    description = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    evolution = scrapy.Field()
    type = scrapy.Field()

class PokemonAttacksItem(scrapy.Item):
    pokemon_id = scrapy.Field()
    attack_list = scrapy.Field()

class AttackItem(scrapy.Item):
    name = scrapy.Field()
    type = scrapy.Field()
#    power = scrapy.Field()
#    accuracy = scrapy.Field()
#    effect = scrapy.Field()



