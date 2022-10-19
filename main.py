from fastapi import FastAPI
import sqlite3
from typing import Union
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from nbsscraper.spiders.nbsspiderPUT import NbsArticleSpiderPUT
import os


app = FastAPI()

def construct_json_output_with_labels(db):
    db_dict = []
    for row in db:
        row_dict = {}
        row_dict['item_id'] = row[0]
        row_dict['date'] = row[1]
        row_dict['url'] = row[2]
        row_dict['labels'] = row[3]
        row_dict['links'] = row[4]
        row_dict['body'] = row[5]
        db_dict.append(row_dict)
    return db_dict

@app.get("/articles/")
def serve_articles(date: Union[str, None] = None, label: Union[str, None] = None):
    
    try:
        con = sqlite3.connect('./nbs_articles.db')
        cur = con.cursor()    

        if date:
            cur.execute(f'SELECT * FROM articles WHERE date={date}')
            database = cur.fetchall()

            return construct_json_output_with_labels(database)

        if label:
            cur.execute('SELECT * FROM articles')
            database = cur.fetchall()
            article_list = []
            for article in database:
                if label in article[3]:
                    article_list.append(article)
                    
            return article_list

        cur.execute('SELECT * FROM articles')
        database = cur.fetchall()

        return construct_json_output_with_labels(database)

    except sqlite3.OperationalError:
        return {"DATABASE IS EMPTY"}


@app.get("/article/{article_id}")
def serve_articles(article_id: int):
    
    try:
        con = sqlite3.connect('./nbs_articles.db')
        cur = con.cursor()    

        cur.execute(f'SELECT * FROM articles WHERE item_id={article_id}')
        database = cur.fetchall()

        return construct_json_output_with_labels(database)


    except sqlite3.OperationalError:
        return {"DATABASE IS EMPTY"}
    
@app.delete("/article/{article_id}")
def serve_articles(article_id: int):
    
    try:
        con = sqlite3.connect('./nbs_articles.db')
        cur = con.cursor()    

        cur.execute(f'DELETE FROM articles WHERE item_id={article_id}')
        con.commit()


    except sqlite3.OperationalError:
        return {"DATABASE IS EMPTY"}



@app.put("/article/{article_id}")
def serve_articles(article_id: int):
    
    os.system(f"scrapy crawl nbsspiderPUT -a article_id={article_id}")
    
