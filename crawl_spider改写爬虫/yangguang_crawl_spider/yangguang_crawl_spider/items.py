# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YangguangCrawlSpiderItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
    state = scrapy.Field()
    code = scrapy.Field()
