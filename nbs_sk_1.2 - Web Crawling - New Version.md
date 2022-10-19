# ADP data colection recruitment task
version 1.2

## Requirements
- Upload your project on [github](https://github.com/).
- Use Python >=3.8.
- Create README.md documentation on how to install and run crawling script and API.
- You have 5 days.

# Data Collection
Collect at least 20 NBS articles from the [nbs.sk](https://nbs.sk/en/press/news-overview/).

## Requirements
- Use [Scrapy Framework](https://scrapy.org/).
- Create and implement [JSON Schema](https://json-schema.org/) validation for the crawled article.
- Use [sqlite3](https://www.sqlite.org/index.html) to store the data.
- Clean up the HTML from the body.
- Extract links from the body of the article if any.
- Make sure that on a second run the spider don't make duplicates in the DB.

# Data delivery
Using the collected data create a REST API.

## Requirements
- Use [Fast API](https://fastapi.tiangolo.com/) (or simmilar framework).
- The API should come with documentation.
- REST API datapoints: 

| Datapoint                | HTTP Method | Description                                   |
| ------------------------ | ----------- | --------------------------------------------- |
| /articles/               | GET         | get all crawled articles and their propertirs |
| /articles/?label={label} | GET         | get list of articles with the same label      |
| /articles/?date={date}   | GET         | get list of articles from the date            |
| /article/{article_id}    | GET         | get single article                            |
| /article/{article_id}    | DELETE      | delete singel article                         |
| /article/{article_id}    | PUT         | update singel article                         |

## Article information example
```JSON
{
  "itme_id": "10",
  "date": "2022-04-20",
  "url": "https://nbs.sk/en/news/nbs-warning-about-axe-capital-group-se/",
  "labels": ["NBS Warning", "Information for Public"],
  "links": ["https://www.instagram.com/axe.capital.group/", "https://www.facebook.com/AxeCapitalGroup/"],
  "body": "Národná banka Slovenska (NBS) warns the public about the activities of AXE Capital Group SE, which offers investment opportunities at the following websites: https://www.instagram.com/axe.capital.group/ and https://www.facebook.com/AxeCapitalGroup/. Please note that this company is currently not subject to supervision by NBS. It is not authorised by NBS to conduct any activity in the Slovak financial market, nor is it recorded in any register maintained by NBS. Funds invested through this company are not covered by Slovakia’s Deposit Protection Fund1 or Investment Guarantee Fund.2 We continue to warn consumers interested in investing in the financial market to consider carefully before concluding a contract with a financial services provider and to check the provider against the list of authorised providers listed on the NBS website. AXE Capital Group SE has its registered office at Štúrova 27, 040 01 Košice (Staré Mesto district) and its company registration number (IČO) is 52 005 666. 1  In accordance with Act No 118/1996 on the protection of deposits (and amending certain laws), as amended. 2  In accordance with Act No 566/2001 on securities and investment services (and amending certain laws), as amended."
}
```
