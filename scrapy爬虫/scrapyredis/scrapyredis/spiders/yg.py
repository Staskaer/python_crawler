import re
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyredis.items import YangguangLoador, YgItem
from scrapy_redis.spiders import RedisSpider


class YgSpider(CrawlSpider, RedisSpider):
    name = 'yg'
    allowed_domains = []
    redis_key = 'yg:start_urls'

    rules = (
        Rule(LinkExtractor(allow=r'/political/politics/index\?id=\d+', restrict_xpaths="//ul[@class='title-state-ul']/li"),
             callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'/political/index/politicsNewest\?id=1&page=\d+'),
             follow=True),
    )

    def parse_item(self, response):
        loador = YangguangLoador(item=YgItem(), response=response)
        loador.add_xpath(field_name='title',
                         xpath="//p[@class='focus-details']/text()")
        loador.add_xpath(field_name='text',
                         xpath="//div[@class='details-box']//text()")
        loador.add_xpath(
            field_name='image', xpath="//div[@class='clear details-img-list Picture-img']/img/@src")
        data = re.findall(
            r"<span class=\"fl\">发布日期(\d+-\d+-\d+ \d+:\d+:\d+)</span>", response.text)
        status_code = re.findall(
            r"<span class=\"fl\">状态：(.*?)</span>", response.text, re.DOTALL)
        id_code = re.findall(
            r"<span class=\"fl\">编号：(\d+)</span>", response.text)
        loador.add_value(field_name='time', value=data)
        loador.add_value(field_name='status', value=status_code)
        loador.add_value(field_name='id_code', value=id_code)
        yield loador.load_item()
