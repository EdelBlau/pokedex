# 1. Instalación del proyecto

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
    
En el siguiente capítulo veremos cómo configurar el spider para extraer información de la web.

# 2. Capturando a Bulbasaur

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

10. Vamos a mostrar por consola los campos que hemos encontrado modificando nuestro spider:

    ```python
    # -*- coding: utf-8 -*-
    import scrapy


    class PokedexSpider(scrapy.Spider):
        name = 'pokedex'
        allowed_domains = ['pokemon.com']
        start_urls = ['https://www.pokemon.com/uk/pokedex/bulbasaur']

        def parse(self, response):
            self.log('----------INFORMACIÓN DE BULBASAUR------------')
            self.log('ID: {}'.format(response.css('div.pokedex-pokemon-pagination-title div span::text')))
            self.log('name: {}'.format(response.css('div.pokedex-pokemon-pagination-title div::text')))
            self.log('description: {}'.format(response.css('div.version-descriptions p.active::text')))
            self.log('evolution: {}'.format( response.css('section.pokedex-pokemon-evolution li span::text')))
            self.log('type: {}'.format(response.css('div.pokedex-pokemon-attributes div.dtm-type ul')))
            self.log('height: {}'.format(response.css('div.pokemon-ability-info ul li')))
            self.log('weight: {}'.format(response.css('div.pokemon-ability-info ul li')))
            self.log('-----------------------------------------------')
    ```

    Y si volvemos a ejecutar el spider, veremos que los datos aparecen, pero no en el formato que nos gustaría...

    ```
    2019-12-04 00:34:36 [pokedex] DEBUG: ID: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/descendant-or-self::*/span/text()" data='#001'>]
    2019-12-04 00:34:36 [pokedex] DEBUG: name: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/text()" data='\n      Bulbasaur\n      '>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-pagination-title ')]/descendant-or-self::*/div/text()" data='\n    '>]
    2019-12-04 00:34:36 [pokedex] DEBUG: description: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' version-descriptions ')]/descendant-or-self::*/p[@class and contains(concat(' ', normalize-space(@class), ' '), ' active ')]/text()" data='\n                  Bulbasaur can be s...'>]
    2019-12-04 00:34:36 [pokedex] DEBUG: evolution: [<Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #001\n        '>, <Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #002\n        '>, <Selector xpath="descendant-or-self::section[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-evolution ')]/descendant-or-self::*/li/descendant-or-self::*/span/text()" data='\n            #003\n        '>]
    2019-12-04 00:34:36 [pokedex] DEBUG: type: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokedex-pokemon-attributes ')]/descendant-or-self::*/div[@class and contains(concat(' ', normalize-space(@class), ' '), ' dtm-type ')]/descendant-or-self::*/ul" data='<ul>\n\t            <li class="backgrou...'>]
    2019-12-04 00:34:36 [pokedex] DEBUG: height: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                    <a href="" c...'>]
    2019-12-04 00:34:36 [pokedex] DEBUG: weight: [<Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                <span class="att...'>, <Selector xpath="descendant-or-self::div[@class and contains(concat(' ', normalize-space(@class), ' '), ' pokemon-ability-info ')]/descendant-or-self::*/ul/descendant-or-self::*/li" data='<li>\n                    <a href="" c...'>]
    2019-12-04 00:34:36 [pokedex] DEBUG: -----------------------------------------------
    ```

11. Vamos a formatear los campos obtenidos para obtenerlo en un formato más legible y útil:

    ```python
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
    ```

    Y comprobamos que ahora la salida tiene un formato mucho más manejable:

    ```
    2019-12-04 00:40:12 [pokedex] DEBUG: ----------INFORMACIÓN DE BULBASAUR------------
    2019-12-04 00:40:12 [pokedex] DEBUG: ID: 001
    2019-12-04 00:40:12 [pokedex] DEBUG: name: Bulbasaur
    2019-12-04 00:40:12 [pokedex] DEBUG: description: Bulbasaur can be seen napping in bright sunlight.
    There is a seed on its back. By soaking up the sun's rays,
    the seed grows progressively larger.
    2019-12-04 00:40:12 [pokedex] DEBUG: evolution: ['001', '002', '003']
    2019-12-04 00:40:12 [pokedex] DEBUG: type: ['Grass', 'Poison']
    2019-12-04 00:40:12 [pokedex] DEBUG: height: 0.7
    2019-12-04 00:40:12 [pokedex] DEBUG: weight: 6.9
    2019-12-04 00:40:12 [pokedex] DEBUG: -----------------------------------------------
    ```