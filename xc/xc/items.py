# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
'''
此文件是生成XCItem
'''


class XcItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    contents = scrapy.Field()
    usr_ID = scrapy.Field()
    usr_name = scrapy.Field()
    img_url_list = scrapy.Field()
