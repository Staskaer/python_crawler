from urllib.parse import quote
import scrapy
from scrapy_splash import SplashRequest
from scrapysplashtest.items import ScrapysplashtestItem


class SplashexSpider(scrapy.Spider):
    name = 'splashex'
    allowed_domains = []

    def start_requests(self):
        url = "https://github.com/search?q=python_crawler"
        #targeturl = 'https://httpbin.org/cookies/set/hello/world'
        lua = '''
        function main(splash,args)
            splash:go('https://httpbin.org/cookies/set/hello/world')
            return splash:get_cookies()
        end
        '''
        # yield scrapy.Request(url="http://localhost:8050/execute?lua_source="+quote(lua), callback=self.parse)
        yield SplashRequest(url=url, callback=self.parse)

    def parse(self, response):
        '''
        # print(response.headers.getlist('Set-Cookie'))
        print(response.text)
        yield scrapy.Request(url='https://httpbin.org/cookies', callback=self.parse)
        '''
        li_list = response.xpath(".//ul[@class='repo-list']/li")
        for li in li_list:
            items = ScrapysplashtestItem()
            items['url'] = li.xpath(
                ".//a[@class= 'v-align-middle']/@href").get()
            yield SplashRequest(url=response.urljoin(items['url']), callback=self.parse_detail, meta={'item': items})

        next_url = response.xpath(".//a[@class= 'next_page']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield SplashRequest(url=next_url, callback=self.parse)

    def parse_detail(self, response):
        items = response.meta['item']
        items['title'] = response.xpath(
            "//strong[@class='mr-2 flex-self-stretch']/a/text()").get()
        items['readme'] = response.xpath(
            ".//div[@class='Box-body px-5 pb-5']//text()").getall()
        items['readme'] = " ".join(items['readme'])
        yield items
