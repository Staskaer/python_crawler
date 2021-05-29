import scrapy
from bs4 import BeautifulSoup


class ItcastSpider(scrapy.Spider):
    name = 'itcast'
    allowed_domains = ['itcast.cn']
    start_urls = ['https://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        # retl = response.xpath(
        #    "/html/body/div[2]/div[11]/div/div[3]/div[1]/div[2]/ul[1]/li[1]/div[3]/h2").extract()
        # print(retl)
        soup = BeautifulSoup(response.text, 'html.parser')
        li = soup.find_all(class_="main_bot")
        for i in li:
            li = {}
            li[i.find('h2').get_text().split("课")[0]] = i.find(
                'h2').get_text().split("师")[1]
            yield li
