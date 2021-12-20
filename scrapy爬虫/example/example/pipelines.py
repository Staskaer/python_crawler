# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import StrictRedis


class ExamplePipeline:
    def process_item(self, item, spider):
        return item

    def open_spider(self, spider):
        print("spider opened")

    def close_spider(self, spider):
        print("spider closed")
