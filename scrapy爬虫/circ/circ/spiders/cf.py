import scrapy
import json
from ..items import CircItem
#from bs4 import BeautifulSoup
#import copy


class CfSpider(scrapy.Spider):
    page_number = 1
    name = 'cf'
    allowed_domains = ['www.cbirc.gov.cn']
    start_urls = [
        'https://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild?itemId=915&pageSize=18&pageIndex='+str(page_number)]

    def parse(self, response):
        item = CircItem()
        lt = json.loads(response.text)["data"]["rows"]
        # print(lt)
        if lt != '':
            for i in lt:
                item["title"] = i["docSubtitle"]
                item["href"] = "https://www.cbirc.gov.cn/cn/view/pages/ItemDetail.html?docId=" + \
                    str(i["docId"])
                item["launch_time"] = i["publishDate"]
                # yield scrapy.Request(
                #    item["href"],
                #    callback=self.parse_data,
                #    meta={"item": copy.deepcopy(item)}
                # )//由于暂时还未能处理由js生成的网页，故先弃之此函数
                yield item
            next_url = "https://www.cbirc.gov.cn/cbircweb/DocInfo/SelectDocByItemIdAndChild?itemId=915&pageSize=18&pageIndex=" + \
                str(self.page_number)
            self.page_number += 1
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def parse_data(self, response):
        pass
        #item = response.meta['item']
        #soup = BeautifulSoup(response.text, 'html.parser')
