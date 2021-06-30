import scrapy
from copy import deepcopy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['amazon.cn']
    start_urls = ['http://www.amazon.cn/gp/book/all_category']

    def parse(self, response):  # 在起始页面上获取大分类的函数
        item = {}
        a_list_b = response.xpath(
            ".//h5[@class = 'a-spacing-top-small a-color-state a-text-bold a-nowrap']/a")
        for a in a_list_b:
            item["b_cate"] = a.xpath(".//text()").extract()[1]
            item["b_href"] = a.xpath(".//@href").extract_first()
            yield scrapy.Request(
                item["b_href"],
                callback=self.get_s_cate,
                meta={"item": deepcopy(item)}
            )

    def get_s_cate(self, response):  # 获取大分类进去后获取小分类
        item = response.meta['item']
        li_list = response.xpath(
            ".//li[@class = 'a-spacing-micro apb-browse-refinements-indent-2']")

        for li in li_list:
            item['s_cate'] = li.xpath(
                ".//span[@dir = 'auto']/text()").extract_first()
            item["s_href"] = li.xpath(".//@href").extract_first()
            yield scrapy.Request(
                response.urljoin(item["s_href"]),
                callback=self.get_book,
                meta={"item": item}
            )

    def get_book(self, response):  # 进入小分类页面，获取到更多从而进入具体页面
        item = response.meta['item']
        url = response.xpath(
            ".//div[@class = 'a-box-inner']/a/@href").extract_first()
        yield scrapy.Request(
            response.urljoin(url),
            callback=self.get_book_info,
            meta={"info": item}
        )

    def get_book_info(self, response):  # 处理翻页和获取每本书的信息
        info = response.meta['info']
        item = {}
        item['b_cate'] = info['b_cate']
        item['s_cate'] = info['s_cate']
        item['price'] = response.xpath(
            ".//span[@class = 'a-offscreen']/text()").extract_first()
        item['name'] = response.xpath(
            ".//span[@class = 'a-size-medium a-color-base a-text-normal']/text()").extract_first()
        yield item
        next_url = response.xpath(
            ".//li[@class = 'a-last']/a/@href").extract_first()
        yield scrapy.Request(
            response.urljoin(next_url),
            callback=self.get_book_info,
            meta={"info": info}
        )
