# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

from neo4j import GraphDatabase, basic_auth
from neomodel import StructuredNode, StringProperty, RelationshipTo, RelationshipFrom, config

class PokemonPipeline(object):

    def process_item(self, item, spider):
        driver = GraphDatabase.driver("bolt://localhost:7687", auth=basic_auth("neo4j", "pokemon12345"))
        session = driver.session()

        print("pokemon_id: " + item['id'])
        query = "MERGE (p_%s:Pokemon {id:'%s', name:'%s', height:%s, weight:%s})" % (item['id'], item['id'], item['name'], item['height'], item['weight'])
        session.run(query)
        for evolution in item['evolution']:
            if int(item['id']) != int(evolution):
                query_2 = "MATCH (p_%s:Pokemon {id:'%s'}) MATCH (p_%s:Pokemon {id:'%s'}) MERGE (p_%s)-[:EVOLUTION]->(p_%s);" % (item['id'],item['id'], evolution, evolution, evolution, item['id'])
                session.run(query_2)
        session.close()

        return item