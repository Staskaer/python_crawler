# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import StrictRedis


class ScrapyseleniumPipeline:

    def __init__(self, host, port, db, password):
        self.db = db
        self.host = host
        self.port = port
        self.password = password

    @classmethod
    def from_crawler(cls, crawler):
        host = crawler.settings.get("REDIS_HOST")
        port = crawler.settings.get("REDIS_PORT")
        db = crawler.settings.get("REDIS_DB")
        password = crawler.settings.get("REDIS_PASSWORD")
        return cls(host, port, db, password)

    def open_spider(self, spider):
        self.client = StrictRedis(host=self.host, port=self.port,
                                  db=self.db, password=self.password)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.client.set(item['title'], item['readme'])
        return item
