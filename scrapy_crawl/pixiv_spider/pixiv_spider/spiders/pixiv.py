import json
from time import sleep
from urllib.parse import urlencode
import scrapy
from pixiv_spider.settings import COOKIES
from pixiv_spider.items import PixivSpiderItem
from copy import deepcopy
import re


class PixivSpider(scrapy.Spider):
    name = 'pixiv'
    # 这是获取搜索类的链接的ajax接口，获取每张图片的id
    baseurl = 'https://www.pixiv.net/ajax/search/artworks/arcaea?'
    # 通过id直接进入到详情页面的Ajax接口，获取图片的原始地址信息
    pic_detail_url = "https://www.pixiv.net/ajax/illust/{}/pages?lang=zh"
    # 这是获取like数量的地址：
    like_count = "https://www.pixiv.net/artworks/{}"
    allowed_domains = []
    page = 1
    data = {'word': 'arcaea', 'order': 'date_d', 'mode': 'all',
            's_mode': 's_tag', 'type': 'all', 'lang': 'zh'}

    def start_requests(self):
        data = self.data
        data['p'] = self.page
        self.page += 1
        targeturl = self.baseurl + urlencode(data)  # 这里获取json第一接口

        self.cookies = {}
        for i in COOKIES.split(';'):
            self.cookies[i.split('=', 1)[0]] = i.split('=', 1)[
                1]  # 这里获取cookies

        yield scrapy.Request(
            url=targeturl,
            callback=self.parse,
            cookies=self.cookies
        )

    def parse(self, response):  # 这个函数请求获取到的目录页面的下的每张图片的id和其他信息
        text = json.loads(response.text)
        data = text.get('body').get('illustManga').get('data')
        total = text.get('body').get('illustManga').get('total')
        if total < 2900:
            print("\n\ncookie 失效！\n\n")
            sleep(5)
        for i in data:
            items = PixivSpiderItem()
            items['id'] = i.get('id')
            items['title'] = i.get('title')
            yield scrapy.Request(
                url=self.like_count.format(items['id']),
                callback=self.parse_likecount,
                cookies=self.cookies,
                meta={'item': items}
            )

        # 翻页处理，这里的翻页处理的不好，应该根据返回的数据是否为空来判断翻页请求
        data = self.data
        data['p'] = self.page
        if self.page < 50:
            self.page += 1
            targeturl = self.baseurl + urlencode(data)
            yield scrapy.Request(
                url=targeturl,
                callback=self.parse,
                cookies=self.cookies
            )

    def parse_likecount(self, response):  # 这个函数处理来获取图片的爱心数目，小于一定数目的就不爬取了
        items = response.meta['item']
        items['likecount'] = re.findall(
            r"\"likeCount\":(\d+)", response.text)[0]
        items['likecount'] = int(items['likecount'])
        if items['likecount'] > 30:
            yield scrapy.Request(
                url=self.pic_detail_url.format(items['id']),
                callback=self.parse_image,
                cookies=self.cookies,
                meta={'item': items}
            )
        else:
            print("one page ignored\n")

    def parse_image(self, response):  # 获取每张图的url地址，传入pipeline
        text = json.loads(response.text)
        url_list = text.get('body')
        num = 1
        for urls in url_list:
            name = '({})'
            items = deepcopy(response.meta['item'])
            items['ori_url'] = urls['urls']['original']
            items['name'] = items['title'] + name.format(num)
            items['name'].replace('\\', '')
            items['name'].replace('/', '')
            num += 1
            yield items
