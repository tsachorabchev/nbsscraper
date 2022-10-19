# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags



# reshufles day, month, year in the correct order
# changes separator
def change_date_format(scraped_date):

    day, month, year = scraped_date.split('. ')

    # makes 2 -> 02 etc.
    def two_digit_format(value):
        if int(value) < 10:
            value = f'0{value}'
        return value

    return f'{year}-{two_digit_format(month)}-{two_digit_format(day)}'

def normalize_space(value):
    return " ".join(value.split())   



class NbsscraperItem(scrapy.Item):

    item_id = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(input_processor = MapCompose(remove_tags, change_date_format), output_processor = TakeFirst())
    url = scrapy.Field(input_processor = MapCompose(remove_tags), output_processor = TakeFirst())
    labels = scrapy.Field(input_processor = MapCompose(remove_tags))
    links = scrapy.Field()
    body = scrapy.Field(input_processor = MapCompose(remove_tags, normalize_space), output_processor = Join())
    
class NbsscraperPutItem(scrapy.Item):

    item_id = scrapy.Field(output_processor = TakeFirst())
    date = scrapy.Field(output_processor = TakeFirst())
    url = scrapy.Field(output_processor = TakeFirst())
    labels = scrapy.Field()
    links = scrapy.Field()
    body = scrapy.Field(input_processor = MapCompose(remove_tags, normalize_space), output_processor = Join())
    
