from copy import deepcopy
import scrapy
from xc.settings import PAGE, json_data, headers
from xc.items import XcItem
import json

'''
此文件是scrapy的爬虫文件，编写处理由downloader下载的response对象
'''


class XiechengSpider(scrapy.Spider):
    page = PAGE
    raw_json = json_data
    name = 'xiecheng'
    allowed_domains = ['m.ctrip.com']
    start_urls = [
        'https://m.ctrip.com/restapi/soa2/13444/json/getCommentCollapseList']

    def start_requests(self):
        # 处理起始请求，由于携程的评论的ajax请求是post方法
        # 所以需要对起始页面单独构造请求
        json_temp = deepcopy(self.raw_json)
        json_temp["arg"]["pageIndex"] = self.page
        self.page += 1
        yield scrapy.Request(
            url=self.start_urls[0],  # 地址
            method="POST",  # 方法
            headers=headers,  # headers
            body=json.dumps(json_temp),  # post数据
            callback=self.parse,  # 回调函数
        )

    def parse(self, response):
        # 处理response的函数
        # 由于ajax返回的为标准json格式，所以直接提取即可

        text = json.loads(response.text)
        items = text['result']['items']  # 获取每页中的所有评论数据

        for i in items:
            item = XcItem()  # 创建Item
            item['contents'] = i['content']
            try:
                # 有一部分评论没有usr_name，不知道为什么
                item['usr_ID'] = i['userInfo']['userId']
                item['usr_name'] = i['userInfo']['userNick']
            except:
                item['usr_ID'] = " "
                item['usr_name'] = " "
            img_list = i['images']
            item['img_url_list'] = []
            for img in img_list:
                item['img_url_list'].append(img['imageSrcUrl'])
            yield item

        # 下面处理翻页
        # 采用deepcopy是为了防止各个并发之间相互干扰
        json_temp = deepcopy(self.raw_json)
        json_temp["arg"]["pageIndex"] = self.page
        self.page += 1
        # 构造下一个请求
        yield scrapy.Request(
            url=self.start_urls[0],
            method="POST",
            headers=headers,
            body=json.dumps(json_temp),
            callback=self.parse,
        )
