# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class StockCrawlSpiderItem(scrapy.Item):
    id = scrapy.Field()
    price_now = scrapy.Field()
    price_highset = scrapy.Field()
    price_lowest = scrapy.Field()
    score = scrapy.Field()
