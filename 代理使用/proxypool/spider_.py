# 为获取模块提供爬虫类


from utils import get_page
from lxml import etree
from urllib.parse import urlencode, urljoin
import re


class ProxyMetaclass(type):
    # 解释：这是一个元类，创建时默认调用__new__
    # 而类通过元类创建时，传递给元类的参数等同于type()函数创建类时的参数列表
    # 作用是通过这个元类来获取到爬虫类中的所有目标网站的爬虫，方便扩展
    def __new__(cls, name, bases, attrs):
        counts = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'Crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                counts += 1
        attrs['__CrawlCount__'] = counts
        return type.__new__(cls, name, bases, attrs)


class Crawler(object, metaclass=ProxyMetaclass):
    def get_proxies(self, callback):
        proxies = []
        for proxy in eval("self.{}()".format(callback)):  # 用callback调用函数
            print("获取代理成功", proxy)
            proxies.append(proxy)
        return proxies

    def Crawl_89api(self, proxycount=50):
        # 此函数调用网站的api，默认提取50个
        print("正在调用89代理的api来获取代理...")
        baseurl = "http://api.89ip.cn/tqdl.html?"
        params = {
            'api': '1',
            'num': proxycount
        }
        url = baseurl + urlencode(params)
        text = get_page(url)
        proxy_list = re.findall(r"(?:\d+\.){3}\d+:\d+", text)
        for proxy in proxy_list:
            yield proxy

    def Crawl_yundaili(self, pagecount=5):
        # 此函数用于爬取云代理的高匿代理，且仅爬取https代理
        print("正在爬取云代理获取代理...")
        page = 1
        baseurl = "http://www.ip3366.net/free/?"
        while page < pagecount:
            params = {
                'stype': 1,
                'page': page
            }
            page += 1
            url = baseurl + urlencode(params)
            text = get_page(url)
            tree = etree.HTML(text)
            tr_list = tree.xpath(
                "//table[@class = 'table table-bordered table-striped']/tbody/tr")
            for tr in tr_list:
                item = tr.xpath("./td/text()")
                if item[3] == 'HTTPS':
                    yield ":".join([item[0], item[1]])

    def crawl_xiaohuan(self, proxycount=100):  # 如需启用此方法注意要把小写改成大写
        # 这个通过调用api的方法似乎在一次更新之后不能使用了
        # 爬取小幻代理
        # 这个网站比较复杂
        # 需要先向这个js网页通过带上referer请求来获取到下面post请求必要的参数
        # 不带referer不能获取到此参数
        print("正在通过小幻代理的api接口获取代理...")
        js_url = "https://ip.ihuan.me/mouse.do"
        api_url = "https://ip.ihuan.me/tqdl.html"
        js_text = get_page(url=js_url, referer='https://ip.ihuan.me/ti.html')
        key = re.findall(r'\.val\("(.*?)"\)', js_text)[0]
        # 获取到key这个关键参数后向api接口网站提交表单
        # 内容包含数目等信息，同时也要包含referer
        data = {
            'num': 100,
            'anonymity': 2,
            'sort': 1,
            'key': key
        }
        text = get_page(
            url=api_url, referer="https://ip.ihuan.me/ti.html", post=True, data=data)
        proxy_list = re.findall(r"(?:\d+\.){3}\d+:\d+", text)
        for proxy in proxy_list:
            yield proxy

    def Crawl_xiaohuan(self, pagecount=5):
        # 小幻代理的爬虫，仅爬取高匿HTTPS代理
        print("正在通过爬取小幻代理来获取代理...")
        count = 1
        url = "https://ip.ihuan.me"
        while count < pagecount:
            text = get_page(url)
            count += 1
            tree = etree.HTML(text)

            next_url = tree.xpath("//a[@aria-label = 'Next']/@href")[0]
            url = urljoin(url, next_url)
            # 翻页url
            tr_list = tree.xpath(
                "//table[@class= 'table table-hover table-bordered']/tbody/tr")
            for tr in tr_list:
                https_avai = tr.xpath("./td[5]/text()")[0]
                if https_avai == '支持':
                    proxy = tr.xpath("./td[1]/a/text()")[0]
                    port = tr.xpath("./td[2]/text()")[0]
                    yield ":".join([proxy, port])
