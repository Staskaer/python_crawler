import scrapy
import re
from copy import deepcopy


class BookSpider(scrapy.Spider):
    url_name = 1
    name = 'book'
    allowed_domains = ['list.jd.com', '360buyimg.com']
    start_urls = [
        'https://misc.360buyimg.com/channel/bookhome/3.0.0/widget/category/category.js']

    def parse(self, response):  # 处理大列表，来获取每个子分类
        type_list = re.findall(re.compile(
            'href="(https://list.jd.com.*?)"'), response.text)
        for type_url in type_list:
            yield scrapy.Request(
                type_url,
                callback=self.parse_type)

    def parse_type(self, response):
        item = {}
        total_list = response.xpath('//ul[@class = "gl-warp clearfix"]/li')
        for li in total_list:
            item['title'] = li.xpath(".//div[@class = 'p-name']/a/em/text()")
            item['price'] = li.xpath(
                ".//div[@class = 'p-price'/strong/i/text()")
            yield item
        '''
        item['title'] = total_list.xpath(
            ".//div[@class = 'p-name']/a/em/text()").extract_first()
        item['price'] = total_list.xpath(
            ".//div[@class = 'p-price']/strong/i/text()").extract_first()'''

        with open('{}.html'.format(self.url_name), 'wb') as f:  # 将网页保存在本地以方便检查是否出现问题
            f.write(response.body)
        self.url_name += 1


# 一些说明的内容：
# jd的商品页每页有60条数据，而单独访问该url地址只会获取到30条数据
# 而在当前页点击下一页是获取到实际第三页的内容，即第60-90条数据
# 因此：直接点击每一页获取到的是奇数页的内容。
# 偶数页的内容是浏览器通ajax请求访问有规律的url地址获得的
# 但是直接访问这个url地址不会获得数据
# 需要带上奇数页内容的url作为referrer来访问才能获得到数据
# 所以，每个小页的处理函数要分开写，从而获得到所有的数据
