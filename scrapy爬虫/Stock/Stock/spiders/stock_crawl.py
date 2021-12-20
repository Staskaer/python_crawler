import scrapy
from bs4 import BeautifulSoup
import re


class StockCrawlSpider(scrapy.Spider):
    name = 'stock_crawl'
    allowed_domains = ['hq.gucheng.com', "xueqiu.com"]  # 允许爬取的域名有两个
    start_urls = [
        'http://hq.gucheng.com/dapangu.html?sort_field_name=px_change_rate&sort_type=desc&page=1']

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")
        a = soup.find_all('a')
        lt = []
        for i in a:
            try:
                href = i.attrs['href']
                code = re.findall(r"[S][HZ]\d{6}", href)[0]
                lt.append(code)
            except:
                continue
        for url in lt:
            stock_url = "https://xueqiu.com/S/" + url
            yield scrapy.Request(
                stock_url,
                callback=self.stock_info,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            )

        if soup.find(class_="stock_page").find_all('a')[6].get_text() == "下一页":
            next_url = soup.find(class_="stock_page").find_all('a')[
                6].attrs['href']
        else:
            next_url = soup.find(class_="stock_page").find_all('a')[
                8].attrs['href']
        if next_url != "":
            next_url = "https://hq.gucheng.com"+next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
                headers={
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36'}
            )

    def stock_info(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        StockInfo = soup.find('div', class_='stock-current').string
        StockName = soup.find(
            'div', 'stock-name').string.split('(')[0]
        item = {}
        item[StockName] = StockInfo
        yield item
