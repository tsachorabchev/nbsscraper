# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3
import json
from jsonschema import validate
from scrapy.exceptions import DropItem




CONTACTS_STRING = "National Bank of SlovakiaCommunications SectionImricha"
MAILING_STRING = "mailinglist"

# (creates database) commits data to the database
class DatabasePipeline:
    def __init__(self):
        self.con = sqlite3.connect('nbs_articles.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS articles(
            item_id INTEGER PRIMARY KEY,
            date TEXT,
            url TEXT,
            labels TEXT,
            links TEXT,
            body TEXT
        )""")


    def process_item(self, item, spider):


        self.cur.execute('''INSERT OR IGNORE INTO articles VALUES(?,?,?,?,?,?)''',
                        (
                            item['item_id'], 
                            item['date'], 
                            item['url'], 
                            json.dumps(item['labels']), 
                            json.dumps(item['links']), 
                            item['body']
                        ))
        self.con.commit()

        return item

# organizes data - truncates body, extracts links
class OrganizeDataPipeline:

    # removes unnecessary parts after the article's body
    def remove_contacts_and_mailing_list_from_body(self, item):

        def truncate_string(target,value_from_where_to_truncate):
            occurence = target.find(value_from_where_to_truncate)
            if occurence > 0:
                target = target[0:occurence].strip()

            return target

        item['body'] = truncate_string(item['body'], CONTACTS_STRING)
        item['body'] = truncate_string(item['body'], MAILING_STRING)


    # extracts links from article body
    def extract_links(self, item):
        body = item['body']
        links = [x for x in body.split() if x.startswith('http://') or x.startswith('https://') or x.startswith('ftp://')]
    

        # cleanse links from accidental punctuation at the end of url
        cleared_links = []
        for link in links:
            while link[-1] in [',', '.', '!', '?', ':', ';']:
                link = link[0:-1]
            
            cleared_links.append(link)

        item['links'] = cleared_links


    def process_item(self, item, spider):

        self.remove_contacts_and_mailing_list_from_body(item)
        self.extract_links(item)
        

        return item
    

# JSON Schema validation
class ValidateDataPipeline:

    def process_item(self, item, spider):

        
        schema = {
            "title": "article",
            "type": "object",
            "properties": {
                "item_id": {"type": "number"},
                "date": {"type": "string"},
                "url": {"type": "string"},
                "labels": {"type": "array"},
                "links": {"type": "array"},
                "body": {"type": "string"},
            },
            "required": ["item_id", "date", "url", "labels", "links", "body"]
        }


        item_json = ItemAdapter(item).asdict()

        validate(instance=item_json, schema=schema)

        return item


# Duplication Check by article URL
class DuplicationCheckPipeline:
    
    def __init__(self):
        self.con = sqlite3.connect('nbs_articles.db')
        self.cur = self.con.cursor()

    def process_item(self, item, spider):

        self.cur.execute('''SELECT url FROM articles''')
        urls_in_database = self.cur.fetchall()
        if (item['url'],) in urls_in_database:
            raise DropItem(f"Duplicate item found: {item!r}")
        else:
            return item
    

