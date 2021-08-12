# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from redis import StrictRedis


class ScrapysplashtestPipeline:
    def process_item(self, item, spider):
        self.client.set(item['title'], item['readme'])

    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.password = password

    @classmethod
    def from_crawler(cls, clawer):
        host = clawer.settings.get('REDIS_HOST')
        port = clawer.settings.get('REDIS_PORT')
        db = clawer.settings.get('REDIS_DB')
        password = clawer.settings.get('REDIS_PASSWORD')
        return cls(host, port, db, password)

    def open_spider(self, spider):
        self.client = StrictRedis(
            host=self.host, port=self.port, db=self.db, password=self.password)

    def close_spider(self, spider):
        self.client.close()
