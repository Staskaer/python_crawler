# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.http import request
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request
from scrapy.exceptions import DropItem


class PixivSpiderPipeline(ImagesPipeline):

    headers = {
        'authority': 'i.pximg.net',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.pixiv.net/',
        'accept-language': 'zh-CN,zh;q=0.9',
        'dnt': '1',
        'sec-gpc': '1',
    }  # 这是每张图片请求必须要携带的headers，否则403

    def get_media_requests(self, item, info):
        yield Request(url=item['ori_url'],  headers=self.headers, meta={'name': item['name']})

    def file_path(self, request, response=None, info=None, *, item=None):
        file_name = request.meta['name'] + '.jpg'
        return file_name

    def item_completed(self, results, item, info):
        image_path = [x['path'] for ok, x in results if ok]
        print("{} has benn downloaded\n".format(item['name']))
        if not image_path:
            raise DropItem('image download failed')
        return item
