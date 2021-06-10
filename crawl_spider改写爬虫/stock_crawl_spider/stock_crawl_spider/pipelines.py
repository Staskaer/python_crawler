# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StockCrawlSpiderPipeline:
    def process_item(self, item, spider):

        print(item["id"])
        print("present price : ", end="")
        print(item["price_now"])
        print('highest price : ', end="")
        print(item['price_highset'])
        print('lowest price : ', end="")
        print(item['price_lowest'])
        print('score : ', end="")
        print(item["score"])
        print('\n')
