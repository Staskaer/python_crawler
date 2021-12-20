import scrapy
from scrapy import item
from ScrapySelenium.items import ScrapyseleniumItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['https://github.com/search?q=python_crawl']

    def parse(self, response):
        li_list = response.xpath("//ul[@class= 'repo-list']/li")
        for li in li_list:
            item = ScrapyseleniumItem()
            item['url'] = li.xpath(".//a[@class='v-align-middle']/@href").get()
            item['url'] = response.urljoin(item['url'])
            yield scrapy.Request(url=item['url'], callback=self.par_detail, meta={'item': item})

        next_url = response.xpath("//a[@class = 'next_page']/@href").get()
        if next_url:
            next_url = response.urljoin(next_url)
            yield scrapy.Request(url=next_url, callback=self.parse)

    def par_detail(self, response):
        try:
            item = response.meta['item']
            item['title'] = response.xpath(
                ".//strong[@class= 'mr-2 flex-self-stretch']/a/text()").get()
            item['readme'] = response.xpath(
                ".//article[@class='markdown-body entry-content container-lg']//text()").getall()

            item['readme'] = ''.join(item['readme'])
            yield item
        except:
            pass
