from types import new_class
import scrapy
from .. items import YangguangItem
from bs4 import BeautifulSoup


class YgSpider(scrapy.Spider):
    name = 'yg'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['https://wz.sun0769.com/political/index/politicsNewest']

    def parse(self, response):
        item = YangguangItem()
        soup = BeautifulSoup(response.text, "html.parser")
        table_list = soup.find_all('li', class_='clear')
        # 构造爬取内容的请求，调用get_content()函数
        for i in table_list:
            item["code"] = i.find(class_='state1').get_text()
            item['state'] = i.find(class_='state2').get_text()
            item['title'] = i.find(class_='state3').get_text()
            item['href'] = "https://wz.sun0769.com" + \
                i.find(class_='color-hover').attrs["href"]
            yield scrapy.Request(
                item['href'],
                callback=self.get_content,
                meta={"item": item}
            )

        # 爬取下一页，调用自身，爬取内容列表
        next_page_url = "https://wz.sun0769.com" + \
            soup.find('a', class_="arrow-page prov_rota").attrs['href']
        temp = next_page_url.split("page=")[1]
        if(temp != "101"):
            print(temp)
            print(next_page_url)
            yield scrapy.Request(
                next_page_url,
                callback=self.parse
            )

    def get_content(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, "html.parser")
        item["content"] = soup.find(class_="details-box").get_text()
        yield item
