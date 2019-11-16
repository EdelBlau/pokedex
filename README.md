

# install with pip
pip3 install virtualenv

virtualenv myvenv

.\myvenv\Scripts\activate

pip install Scrapy

# install with conda
conda create --name venv python=3.7

conda activate venv

conda install -c conda-forge scrapy

# Creating a new Scrapy project

scrapy startproject tutorial

# run spider

scrapy crawl quotes

# shell

scrapy shell 'http://quotes.toscrape.com/page/1/'
response.css('title')
response.css('title::text').getall()
response.xpath('//title/text()').get()

# store data

scrapy crawl quotes -o quotes.json

# Changing spider to recursively follow links

response.css('li.next a::attr(href)').get()
response.css('li.next a').attrib['href']

for href in response.css('li.next a::attr(href)'):
    yield response.follow(href, callback=self.parse)

# Using spider arguments

scrapy crawl quotes -o quotes-humor.json -a tag=humor

    def __init__(self, *args, **kwargs):

        super(QDQSpider, self).__init__(*args, **kwargs)
        self.start_urls = [
            "http://es.qdq.com/"+ kwargs.get('category') +"/"
        ]

# middleware

process_spider_input(response, spider):
    if response.status == 200
        #do what ever you want
        print 'OK 200'
    else: 
    	print 'error on request. Retry'