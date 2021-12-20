import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import re
import os


class TankSpider(CrawlSpider):
    name = 'tank'
    allowed_domains = []
    start_urls = ['https://tieba.baidu.com/p/7301467228']
    picname = 0
    num = 0

    rules = (
        # 此条规则不生效
        # Rule(
        #    LinkExtractor(
        #        allow=r'http://tiebapic.baidu.com/forum/w%3D580/sign=.*?\.jpg'),
        #    callback='parse_item'),

        # 翻页
        Rule(
            LinkExtractor(
                allow=r'/p/\d+\?pn=\d+'),
            callback='parse_item',
            follow=True),
    )

    def parse_item(self, response):  # 爬取帖子内的所有图片
        href = re.findall(re.compile(
            "http://tiebapic.baidu.com/forum/w%3D580/sign=.*?\.jpg"), response.text)
        for url in href:
            yield scrapy.Request(
                url,
                callback=self.save_raw
            )

    def save_raw(self, response):  # 将图片保存在本地

        root = str(os.getcwd()) + "\image_raw\\"
        isexist = os.path.exists(root.rstrip("\\"))
        if not isexist:
            os.makedirs(root.rstrip("\\"))
        while True:  # 当保存失败时重复保存直至成功
            try:
                with open(root + str(self.picname)+".jpg", 'xb') as f:
                    f.write(response.body)
                    self.picname += 1
                    self.num += 1
                    break
            except FileExistsError:  # 保存失败，说明文件名重复
                self.picname += 1
                self.num += 1
