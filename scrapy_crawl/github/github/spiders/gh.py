from operator import pos
import scrapy
import re

# post实现模拟登录的两种方式


class GhSpider(scrapy.Spider):
    name = 'gh'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        # 方法一，直接通过对比原网页post请求来找出对应的字段，提取数据后post
        '''
        commit = response.xpath(
            "//input[@name='commit']/@value").extract_first()
        authenticity_token = response.xpath(
            "// input[@name= 'authenticity_token']/@value").extract_first()
        login = "Fught197075512"
        password = "O33bf0797"
        timestamp = response.xpath(
            "//input[@name = 'timestamp']/@value").extract_first()
        timestamp_secret = response.xpath(
            "//input[@name = 'timestamp_secret']/@value").extract_first()
        post_data = dict(
            commit=commit,
            authenticity_token=authenticity_token,
            login=login,
            password=password,
            timestamp=timestamp,
            timestamp_secret=timestamp_secret
        )

        yield scrapy.FormRequest(
            "https://github.com/session",
            formdata=post_data,
            callback=self.after_login
        )

        '''
        # 方法二 利用FormRquest来查找对应的action从而模拟用户进行数据提交来实现登录
        yield scrapy.FormRequest.from_response(
            response=response,
            formdata={
                "login": "Fught197075512", "password": "O33bf0797"
            },
            callback=self.after_login
        )

    def after_login(self, response):

        with open(r"D:\vs_code_files\python\projects\爬虫\scrapy爬虫\github\a.html", 'w', encoding='utf-8') as f:
            f.write(response.body.decode())
        item = {}
        item['items'] = re.findall("Fught197075512", response.text)
        yield item
