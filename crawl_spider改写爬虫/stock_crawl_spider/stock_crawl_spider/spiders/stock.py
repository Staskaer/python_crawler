import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import StockCrawlSpiderItem
import re
import copy
import json


class StockSpider(CrawlSpider):
    name = 'stock'
    allowed_domains = ['gucheng.com']
    start_urls = [
        'http://hq.gucheng.com/dapangu.html?sort_field_name=px_change_rate&sort_type=desc&page=1']
    rules = (
        Rule(
            LinkExtractor(
                allow=r'dapangu.html\?sort_field_name=px_change_rate&sort_type=desc&page=\d+'),
            follow=True
        ),
        Rule(
            LinkExtractor(
                allow=r'/SZ\d+/'),
            callback='parse_item'
        ),
    )

    def parse_item(self, response):
        item = StockCrawlSpiderItem()
        item["id"] = re.findall(re.compile("<h1>(.*?)</h1>"), response.text)[0]
        item["price_now"] = re.findall(re.compile(
            '<em class="color_up">(.*?)</em>'), response.text)[0]
        item["price_highset"] = re.findall(re.compile(
            '<dd class="color_up">(.*?)</dd>'), response.text)[0]
        item["price_lowest"] = re.findall(re.compile(
            '<dd class="color_up">(.*?)</dd>'), response.text)[1]
        url = "https://api.gucheng.com/lg/zg/base.php?code=" + \
            re.findall("SZ(\d+)", response.text)[0]
        yield scrapy.Request(
            url,
            callback=self.get_score,
            meta={"items": copy.deepcopy(item)}
        )

    def get_score(self, response):
        try:
            item = response.meta["items"]
            item["score"] = json.loads(response.text)[
                "data"]['baseInfo']['score']['score']
            yield item
        except:
            pass
