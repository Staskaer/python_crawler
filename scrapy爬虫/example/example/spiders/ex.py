import scrapy


class ExSpider(scrapy.Spider):
    name = 'ex'
    allowed_domains = []
    start_urls = ['http://httpbin.org/ge78t']
    flag = True

    def start_requests(self):
        print("\n\n\nsuccess\n\n\n")
        return [scrapy.Request(url="http://httpbin.org/get", callback=self.parse)]

    def parse(self, response):
        print(response.status)
        print(response.text)
        if self.flag:
            yield scrapy.Request(url='https://httpbin.org/json', callback=self.parse)
            self.flag = False
