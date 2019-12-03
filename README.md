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