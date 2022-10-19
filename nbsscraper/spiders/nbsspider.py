import scrapy
from scrapy_playwright.page import PageMethod
from nbsscraper.items import NbsscraperItem
from scrapy.loader import ItemLoader
import sqlite3


class NbsArticleSpider(scrapy.Spider):
    def __init__(self,p: int = 5, *args, **kwargs):
        self.start_page = 1
        self.pages_to_crawl = int(p)
        self.end_page = self.pages_to_crawl + self.start_page - 1
        
        super().__init__(**kwargs) 

    # scraper/ spider name
    name = 'nbsspider'
    
    # base URL
    base_url = 'https://nbs.sk/en/press/news-overview/'

    # custom headers
    headers = {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:103.0) Gecko/20100101 Firefox/103.0'
    }

    # related to pagination
    FIRST_PART_OF_PAGINATION_QUERY = """?table_post-list_params={"offset"%3A"""
    SECOND_PART_OF_PAGINATION_QUERY = """%2C"filter"%3A{"lang"%3A"en"}}"""

    
    next_article_id = 1

    # id for the next article (takes max id from DB and adds 1)
    def next_id(id):
        try:
            con = sqlite3.connect('nbs_articles.db')
            cur = con.cursor()
            cur.execute('SELECT item_id FROM articles')
            ids_in_database = cur.fetchall()
            max_id = 0
            for id_db in ids_in_database:
                if max_id < id_db[0]:
                    max_id = id_db[0]
                id = max_id + 1
        except sqlite3.OperationalError:
            print("SQLITE DATABASE IS EMPTY") 

        return id

    next_article_id = next_id(next_article_id)


    # crawler's entry point
    def start_requests(self):


        yield scrapy.Request(
            url=self.base_url,
            meta=dict(
                playwright=True,
                playwright_include_page=True,
                playwright_page_methods=[
                    PageMethod("wait_for_selector", "div.archive-results"),
                ],
            ),
        )


    def parse(self, response):


        for article in response.css('a.archive-results__item'):

            itemloader = ItemLoader(item = NbsscraperItem(), selector = article)

            # populating date, url and labels
            itemloader.add_css('date', 'div.date')
            itemloader.add_css('url', 'a.archive-results__item::attr(href)')
            itemloader.add_css('labels', 'div.label.label--sm')
            itemloader.add_value('links', '')
            

            article_url = article.css('a.archive-results__item::attr(href)').get()

            # creating request for the article's body
            request = scrapy.Request(
                url = article_url,
                callback = self.parse_article_body,
                meta = {'item': itemloader.load_item()},
                dont_filter = True
            )

            yield request

        # next page link creation
        def generate_next_page_url():

            start_article_num = self.start_page * 5
            self.start_page += 1
            
            return f"{self.base_url}{self.FIRST_PART_OF_PAGINATION_QUERY}{start_article_num}{self.SECOND_PART_OF_PAGINATION_QUERY}"

        # pagination
        if self.start_page < self.end_page:

            next_page_url = generate_next_page_url()

            yield scrapy.Request(next_page_url, meta=dict(
                playwright = True,
                playwright_include_page = True, 
                playwright_page_methods =[
                    PageMethod('wait_for_selector', 'div.archive-results'),
                ],
            ))


    # parsing the body of the article
    def parse_article_body(self, response):

        itemloader_body = ItemLoader(
            item=response.meta['item'],
            response=response
            )
        
        # populating the "body" entry
        itemloader_body.add_css('body', 'div.nbs-post__content,div.nbs-content>div,div.nbs-content>ul')
        itemloader_body.add_value('item_id', self.next_article_id)


        self.next_article_id += 1

        return itemloader_body.load_item()
