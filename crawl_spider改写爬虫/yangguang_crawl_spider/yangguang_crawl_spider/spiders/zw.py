import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import YangguangCrawlSpiderItem
import re


class ZwSpider(CrawlSpider):
    name = 'zw'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']

    rules = (
        Rule(LinkExtractor(
            allow=r'/political/politics/index\?id=\d+'),
            callback='parse_item'),
        Rule(LinkExtractor(
            restrict_xpaths="/html/body/div[2]/div[3]/div[3]/a[2]"),
            follow=True,),
    )

    def parse_item(self, response):
        item = YangguangCrawlSpiderItem()
        item["code"] = re.findall(
            '<span class="fl">编号：(\d+)</span>', response.text)[0]
        item["title"] = re.findall(
            '<p class="focus-details">(.*?)</p>', response.text)[0]
        item["content"] = re.findall(re.compile(
            '<pre>(.*?)</pre>', re.DOTALL), response.text)[0]
        item["state"] = re.findall(re.compile(
            '<span class="fl">状态：(.*?)</span>', re.DOTALL), response.text)[0]
        yield item
