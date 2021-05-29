# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class StockPipeline:
    def process_item(self, item, spider):
        for i in item.items():
            print("股票名称 : "+i[0]+"  股票价格:"+i[1])

        return item
