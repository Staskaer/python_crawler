# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class YangguangPipeline:
    def process_item(self, item, spider):
        item["state"] = item["state"].strip("\n ")
        item["content"] = item["content"].strip("\n")
        print("\t编码 ：" + item["code"])
        print("\t标题 ：" + item["title"])
        print("\t内容 ： " + item["content"])
        print("\t状态 ：" + item["state"])
        print("\n")
        return item
