# NBS Article Scraper
## Description
Web Scraper for nbs.sk

extracts the following fields:
- url
- date
- labels
- links
- body

## Dependancies
To run the NBS Article Scraper you need to install
- Scrapy
- Scrapy-playwright
- JSON Schema
- Fast API

# Data Collection
## Instructions
To scrape articles use

$ scrapy crawl nbsspider

The default is 5 pages.
You can use the optional argument "p" to set the number of pages to be scraped.
For example to scrape the first 20 pages use

$ scrapy crawl nbsspider -a p=20

# API
## Instructions
To start the API server use

uvicorn main:app --reload

## Datapoints

| Datapoint                | HTTP Method | Description                                   |
| ------------------------ | ----------- | --------------------------------------------- |
| /articles/               | GET         | get all crawled articles and their properties |
| /articles/?label={label} | GET         | get list of articles with the same label      |
| /articles/?date={date}   | GET         | get list of articles from the date            |
| /article/{article_id}    | GET         | get single article                            |
| /article/{article_id}    | DELETE      | delete singel article                         |
| /article/{article_id}    | PUT         | update singel article                         |

