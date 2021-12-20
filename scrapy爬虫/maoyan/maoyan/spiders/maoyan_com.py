import scrapy
from ..items import MaoyanItem
import urllib.parse


class MaoyanComSpider(scrapy.Spider):
    name = 'maoyan.com'
    allowed_domains = ['maoyan.com']
    start_urls = ['https://maoyan.com/board/4']

    def parse(self, response):
        total_films = response.xpath("//dl[@class='board-wrapper']/dd")
        for film in total_films:
            items = MaoyanItem()
            items['name'] = film.xpath(
                ".//p[@class = 'name']/a/text()").extract_first()
            items['time'] = film.xpath(
                ".//p[@class = 'releasetime']/text()").extract_first()
            items['role'] = film.xpath(
                ".//p[@class = 'star' ]/text()").extract_first().strip('\n ')
            yield items
        try:
            next_url = response.xpath(
                "//a[text()='下一页']/@href").extract_first()
            next_url = urllib.parse.urljoin(response.url, next_url)
            yield scrapy.Request(
                url=next_url,
                callback=self.parse
            )
        except:
            pass
