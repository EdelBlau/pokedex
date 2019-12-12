# Scrapy, ¡hazte con todos (los datos)!

En este repo encontrarás el material del taller de scrapy preparado por [Irene Fernández](https://github.com/EdelBlau) y con adaptaciones por [Alicia Pérez](https://github.com/aliciapj)

## Índice
* [Instalación del proyecto](#instalación-del-proyecto)
* [1. Configurando las requests iniciales](#1-configurando-las-requests-iniciales)
* [2. Generamos un iterable con los datos extraídos](#2-generamos-un-iterable-con-los-datos-extraídos)
* [3. Formateando el contenido de la página con selectores](#3-formateando-el-contenido-de-la-página-con-selectores)
* [4. Almacenando los datos en un fichero](#4-almacenando-los-datos-en-un-fichero)


# Instalación del proyecto

1. Asegúrate de que tienes Python instalado con una versión superior a la 3.4

2. Crea un virtual environment para el proyecto:
    ```bash
    $ python3 -m venv venv
    ```

3. Instala la librería de scrapy:
    ```
    $ pip install scrapy
    ```

4. Crea un proyecto de scrapy llamado `tutorial`:
    ```
    $ scrapy startproject tutorial
    ```
    Ésto te creará la siguiente estructura de carpetas:
    ```
    tutorial
    - scrapy.cfg
    - tutorial/
        - items.py  
        - middlewares.py 
        - pipelines.py 
        - settings.py 
        - spiders/
    ```
    
5. A continuación, sitúate en la carpeta `tutorial` y crea un nuevo spider para la página que vamos a utilizar en el taller (`pokemon.com`):
    ```
    $ cd tutorial
    $ scrapy genspider pokedex 'pokemon.com'
    ```
    Ésto te generará un fichero `pokedex.py` dentro de la carpeta `spiders/` con el siguiente contenido:
    ```python
    # -*- coding: utf-8 -*-
    import scrapy
    
    
    class PokedexSpider(scrapy.Spider):
        name = 'pokedex'
        allowed_domains = ['pokemon.com']
        start_urls = ['http://pokemon.com/']
    
        def parse(self, response):
            pass

    ```
    
6. En este punto ya podríamos ejecutar el spider con el siguiente comando:
    ```bash
    $ scrapy crawl pokedex
    ```
    Pero no veremos ningún resultado porque no le hemos indicado al spider qué debe de descargar ni donde.
    
Generalmente el ciclo de scraping pasa por algo como esto:

* Configuramos las requests iniciales para rastrear las primeras URL y especificamos una función de callback que se llamará con la respuesta de esas requests.
Las primeras requests se obtienen llamando al método `start_requests()` que (por defecto) genera requests para las URLs especificadas en el parámetro `start_urls` del spider y el método de `parse` que devolverá los datos de esas requests.

* En la función de `callback`, analizamos la respuesta (página web) y devolvemos `diccionarios`, objetos `Item`, objetos `Request` o un iterable con los datos extraídos.

* En las callback, formatearemos el contenido de la página, generalmente usando `Selectors` (aunque también podemos usar `BeautifulSoup`, `lxml` o cualquier mecanismo que prefiramos) y generaremos elementos con los datos analizados.

* Por último, los datos obtenidos por la araña generalmente se almacenarán en una base de datos o se escribirán en un archivo usando `Feed exports`.


# 1. Configurando las requests iniciales

7. Añadimos la url de bulbasaur al fichero del spider `pokedex.py` y añadimos el siguiente código de python para descargar el html en un fichero local:
    ```python
    # -*- coding: utf-8 -*-
    import scrapy


    class PokedexSpider(scrapy.Spider):
        name = 'pokedex'
        allowed_domains = ['pokemon.com']
        start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

        def parse(self, response):
            filename = 'bulbasaur.html'
            with open(filename, 'wb') as f:
                f.write(response.body)
            self.log('Saved file %s' % filename)

    ```

8. Ejecutamos el spider:
    ```bash
    $ scrapy crawl pokedex
    ```
    
    Entre las numerosas líneas de consola que aparecen, comprobamos que una de ellas dice lo siguiente:
    
    ```$bash
    2019-12-04 00:20:32 [pokedex] DEBUG: Saved file bulbasaur.html
    ```
    Ahora podemos abrir el fichero `bulbasaur.html` que se ha creado en la raíz del proyecto y estudiar la información que queremos extraer

9. Inspeccionamos los campos del css del fichero descargado para buscar la información que define a `Bulbasaur` y encontramos la siguiente relación de características:
    * Id & nombre
    ```html
    <div class="pokedex-pokemon-pagination-title">
        <div>
        Bulbasaur
        <span class="pokemon-number">#001</span>
        </div>
    </div>
    ```

    * Descripción:
    ```html
    <div class="version-descriptions active">
                    <p class="version-x">
                    Bulbasaur can be seen napping in bright sunlight.
    There is a seed on its back. By soaking up the sun&#39;s rays,
    the seed grows progressively larger.
                    </p>
                
                    <p class="version-yactive">
                    Bulbasaur can be seen napping in bright sunlight.
    There is a seed on its back. By soaking up the sun&#39;s rays,
    the seed grows progressively larger.
                    </p>
            </div>
    ```
    Prueba a encontrar más campos interesantes en el html (evolución, tipo, altura, peso...)

# 2. Generamos un iterable con los datos extraídos

Vamos a almacenar la información extraída del html en items de Scrapy. 
Tienes más info sobre los items en el [tutorial de Scrapy](https://docs.scrapy.org/en/latest/topics/items.html)

10. Creamos una clase `PokemonItem` en nuestro fichero `tutorial/items.py` como vemos a continuación:
    ```python
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
    ```

11. Modificamos nuestro spider para que almacene la información en el item que acabamos de crear:
    ```python
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
            pokemon['id'] = response.css('div.pokedex-pokemon-pagination-title div span::text')
            pokemon['name'] = response.css('div.pokedex-pokemon-pagination-title div::text')
            pokemon['description'] = response.css('div.version-descriptions p.active::text')
            pokemon['evolution'] = response.css('section.pokedex-pokemon-evolution li span::text')
            pokemon['type'] = response.css('div.pokedex-pokemon-attributes div.dtm-type ul')
            pokemon['height'] = response.css('div.pokemon-ability-info ul li')
            pokemon['weight'] = response.css('div.pokemon-ability-info ul li')

            self.log(pokemon)
    ```

    Volvemos a lanzar el spider y comprobamos que todo sigue funcionando bien, pero el formato de salida no es el más adecuado:
    ```bash
    2019-12-04 17:39:11 [pokedex] DEBUG: {'ID': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/descendant-or-self::*/span/text()" data='#001'>], 'name': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/text()" data='\n      Bulbasaur\n      '>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/text()" data='\n    '>], 'description': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' version-descriptions ')]/descendant-or-self::*/p[@class and contains(concat(' ', normalize-space(@class), ' '), ' active ')]/text()" data='\n                  Bulbasaur can be s...'>], 'evolution': [<Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #001\n        '>, <Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #002\n        '>, <Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #003\n        '>], 'type': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-attributes ')]/descendant-or-self::*/div[@class and contains(concat(' ', normalize-space(@class), ' '), ' dtm-type ')]/descendant-or-self::*/ul" data='<ul>\n\t            <li class="backgrou...'>], 'height': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                    <a href="" c...'>], 'weight': [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                    <a href="" c...'>]}
    ```

# 3. Formateando el contenido de la página con selectores

11. Vamos a incluir algunos selectores en nuestro spider para formatear la salida. Tienes más información sobre los selectores en el [tutorial](https://docs.scrapy.org/en/latest/topics/selectors.html#topics-selectors):

    ```python
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
            pokemon['name'] = response.css('div.pokedex-pokemon-pagination-title div::text')
            pokemon['description'] = response.css('div.version-descriptions p.active::text')
            pokemon['evolution'] = response.css('section.pokedex-pokemon-evolution li span::text').re('[0-9]{3}')
            pokemon['type'] = response.css('div.pokedex-pokemon-attributes div.dtm-type ul')[0].css("li a::text").extract()
            pokemon['height'] = response.css('div.pokemon-ability-info ul li')[0]\
                                    .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")
            pokemon['weight'] = response.css('div.pokemon-ability-info ul li')[1]\
                                    .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")

            self.log(pokemon)
    ```

    Volvemos a lanzar el spider y comprobamos que ahora el formato sí es el que buscamos:

    ```python
    2019-12-04 17:45:15 [pokedex] DEBUG: {'description': 'Bulbasaur can be seen napping in bright sunlight.\n'
                    "There is a seed on its back. By soaking up the sun's rays,\n"
                    'the seed grows progressively larger.',
    'evolution': ['001', '002', '003'],
    'height': '0.7',
    'id': '001',
    'name': 'Bulbasaur',
    'type': ['Grass', 'Poison'],
    'weight': '6.9'}
    ```

# 4. Almacenando los datos en un fichero

12. Para poder trabajar con los datos extraidos por el spider, necesitamos que la función de callback, en este caso la de `parse` devuelva el item a Scrapy para su procesamiento. Para ello, sustituimos la traza de log por un `yield` como ves a continuación:

    ```python
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
            pokemon['height'] = response.css('div.pokemon-ability-info ul li')[0]\
                                    .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")
            pokemon['weight'] = response.css('div.pokemon-ability-info ul li')[1]\
                                    .css("span.attribute-value::text").re_first(r'\d{1,2}[\,\.]{1}\d{1,2}').replace(",", ".")

            yield pokemon
    ```

13. Con ésto, ya podemos utilizar el comando que nos provee Scrapy para exportar el resultado del spider a un json:
    ```bash
    $ scrapy crawl pokedex -o pokedex.json
    ```

    Ésto nos generará un fichero `pokedex.json` en la raíz del proyecto con un contenido como el siguiente:
    ```json
    [
    {"id": "001", "name": "Bulbasaur", "description": "Bulbasaur can be seen napping in bright sunlight.\nThere is a seed on its back. By soaking up the sun's rays,\nthe seed grows progressively larger.", "evolution": ["001", "002", "003"], "type": ["Grass", "Poison"], "height": "0.7", "weight": "6.9"}
    ]
    ```

