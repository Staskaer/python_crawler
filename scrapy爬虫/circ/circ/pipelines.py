# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class CircPipeline:
    def process_item(self, item, spider):
        print("\t发布时间 : ", item["launch_time"])
        print("\t标题 : ", item["title"])
        print("\n")
        return item


