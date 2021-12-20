import scrapy
from urllib.parse import urlencode
from image360.items import Image360Item
import json


class ImagesSpider(scrapy.Spider):
    name = 'images'
    allowed_domains = ['images.so.com']

    def start_requests(self):
        data = {
            'ch': 'beauty'
        }
        baseurl = 'https://image.so.com/zjl?'
        for i in range(0, self.settings.get("MAX_PAGE")):
            data['sn'] = i*30
            url = baseurl + urlencode(data)
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get('list'):
            item = Image360Item()
            item['id'] = image.get("id")
            item['url'] = image.get("qhimg_url")
            yield item
