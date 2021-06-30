import scrapy
from copy import deepcopy


class BookSpider(scrapy.Spider):
    name = 'book'
    allowed_domains = ['dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        total = response.xpath("//div[@class= 'con flq_body']/div")
        for div in total:
            # 获取书的大分类
            item = {}
            item['b_cate'] = div.xpath("./dl/dt//text()").extract()
            item['b_cate'] = [i.strip()
                              for i in item['b_cate'] if len(i.strip()) > 0]
            # 书的中间分类标签
            dl_list = div.xpath("./div//dl[@class = 'inner_dl']")
            for dl in dl_list:
                item['m_cate'] = dl.xpath("./dt//text()").extract()
                item['m_cate'] = [i.strip()
                                  for i in item['m_cate'] if len(i.strip()) > 0][0]
                # 小分类
                a_list = dl.xpath("./dd/a")
                for a in a_list:
                    if a.xpath("./text()").extract_first() in ["更多>>>", "更多"]:
                        continue
                    item['s_href'] = a.xpath("./@href").extract_first()
                    item['s_cate'] = a.xpath("./text()").extract_first()
                    if item['s_href'] is not None:
                        yield scrapy.Request(
                            item['s_href'],
                            callback=self.parse_books,
                            meta={"item": deepcopy(item)}
                        )

    def parse_books(self, response):
        info = response.meta['item']  # info是一个不断传递的分类信息，每本书都要包含
        item = {}
        item['b_cate'] = info['b_cate']
        item['m_cate'] = info["m_cate"]
        item["s_cate"] = info["s_cate"]
        li_list = response.xpath(".//ul[@class='bigimg']/li")
        for li in li_list:  # 获取到每本书的信息
            item['name'] = li.xpath(
                ".//p[@class = 'name']/a/text()").extract_first()
            item['price'] = li.xpath(
                ".//span[@class = 'search_now_price']/text()").extract_first()
            yield item

        try:  # 构造翻页请求,重复传递分类信息
            next_url = response.xpath(
                "//li[@class = 'next']/a/@href").extract_first()
            next_url = "http://category.dangdang.com" + next_url
            print(next_url)
            yield scrapy.Request(
                next_url,
                callback=self.parse_books,
                meta={"item": info}
            )
        except:
            pass
