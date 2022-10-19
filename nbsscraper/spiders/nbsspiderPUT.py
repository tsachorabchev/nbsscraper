import scrapy
from scrapy_playwright.page import PageMethod
from nbsscraper.items import NbsscraperPutItem
from scrapy.loader import ItemLoader
import sqlite3


class NbsArticleSpiderPUT(scrapy.Spider):

    # def __init__(self, *a, **kw):
    #     super(NbsArticleSpiderPUT, self).__init__(*a, **kw)

    def __init__(self, article_id, *args, **kwargs):
        self.article_id = article_id
        try:
            con = sqlite3.connect('nbs_articles.db')
            cur = con.cursor()
            cur.execute(f'SELECT * FROM articles WHERE item_id={self.article_id}')
            db_article = cur.fetchone()
        
            self.item_id = db_article[0]
            self.date = db_article[1]
            self.url = db_article[2]
            self.labels = db_article[3]
            self.links = db_article[4]

            cur.execute(f'DELETE FROM articles WHERE item_id={self.article_id}')
            con.commit()
        except:
            print("RECORD NOT FOUND") 

        super().__init__(**kwargs)  

    # scraper/ spider name
    name = 'nbsspiderPUT'
    
    # id of the updated article
    # article_id = 0
    

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    #  extracts data from the old article

    

    # crawler's entry point
    def start_requests(self):
        urls = [
            self.url,
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):

        itemloader = ItemLoader(item = NbsscraperPutItem(), selector = response)


        # populating with database data
        itemloader.add_value('item_id', self.item_id)
        itemloader.add_value('date', self.date)
        itemloader.add_value('url', self.url)
        itemloader.add_value('labels', self.labels)
        itemloader.add_value('links', self.links)

        # parsing new body
        itemloader.add_css('body', 'div.nbs-post__content,div.nbs-content>div,div.nbs-content>ul')

        return itemloader.load_item()
  

