# 爬虫主体模块

from requests import Session
from requests.models import Request
from RedisQueue_ import RedisQueue
from Requests_ import WinxinRequests
from urllib.parse import urlencode
from urllib.parse import urljoin
import requests
from lxml import etree
from requests import ReadTimeout, ConnectionError
from settings import API_ADDRESS
from settings import MAX_FAILED_TIMES
from settings import VALID_CODE


class Spider():
    base_url = "https://weixin.sogou.com/weixin"
    keyword = 'Python'
    headers = {
        'authority': 'weixin.sogou.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'sec-ch-ua': '"Chromium";v="92", " Not A;Brand";v="99", "Google Chrome";v="92"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cookie': 'ABTEST=6|1628238350|v1; SNUID=A1CA44215054988E992B85FE519BB589; SUID=F09A15703F18960A00000000610CF20E; SUV=000A177E70159AF0610CF20EA3394070; SUID=F09A1570565D960A00000000610CF20E; weixinIndexVisited=1; JSESSIONID=aaamY9ezcXEZ4hYkf9_Ox; IPLOC=CN3204; PHPSESSID=ap0eckrvan2k9l1rc114di4lo2; refresh=1',
        'dnt': '1',
        'sec-gpc': '1',
    }
    session = Session()
    queue = RedisQueue()

    def get_proxy(self):
        # 获取一个代理
        try:
            r = requests.get(API_ADDRESS)
            if r.text:
                return r.text
            return ""
        except:
            return ""

    def start(self):
        # 起始地址
        self.session.headers.update(self.headers)
        start_url = self.base_url + '?' + \
            urlencode({'query': self.keyword, 'type': 2})
        weixin_request = WinxinRequests(
            url=start_url, callback=self.parse_index, need_proxy=True)
        self.queue.add(weixin_request)

    def parse_index(self, response):
        # 处理目录页
        tree = etree.HTML(response.text)
        li_list = tree.xpath("//div[@class = 'news-box']/ul/li")
        for li in li_list:
            title_cont = li.xpath(".//div[@class = 'txt-box']/h3//text()")
            fir, *title_list, last = title_cont
            title = "".join(title_list)
            print(title)

            href = li.xpath(".//div[@class='txt-box']/h3/a/@href")[0]
            href = urljoin(base=self.base_url, url=href)

            weixinrequests = WinxinRequests(
                url=href, callback=self.parse_detail)
            yield weixinrequests

        try:
            next_url = tree.xpath("//a[@id = 'sogou_next']/@href")[0]
        except:
            next_url = ''
        if next_url:
            next_url = urljoin(self.base_url, next_url)
            next_requests = WinxinRequests(
                url=next_url, callback=self.parse_index, need_proxy=True)
            yield next_requests

    def parse_detail(self, response):
        # 处理详情页
        # 详情页具有重定向的js代理来处理
        # 此处不对js代码进行分析了
        # 假装处理成功
        # print("detail_ok")
        yield "1"

    def request(self, weixin_requests):
        # 请求加载
        try:
            if weixin_requests.need_proxy:
                proxy = self.get_proxy()
                if proxy:
                    proxies = {
                        'http': 'http://'+proxy,
                        'https': 'https://'+proxy
                    }
                    return self.session.send(weixin_requests.prepare(), timeout=weixin_requests.timeout, allow_redirects=False, proxies=proxies)
            return self.session.send(weixin_requests.prepare(), timeout=weixin_requests.timeout, allow_redirects=False)
        except (ConnectionError, ReadTimeout) as e:
            print(e.args)
            return False

    def error(self, weixin_request):
        # 处理错误
        weixin_request.fail_time = weixin_request.fail_time + 1
        print(weixin_request.url, "fail", weixin_request.fail_time, 'times')
        if weixin_request.fail_time < MAX_FAILED_TIMES:
            self.queue.add(weixin_request)

    def schedule(self):
        # 调度器
        while not self.queue.empty():
            weixin_requests = self.queue.pop()
            callback = weixin_requests.callback
            print("\nSchedule ",)
            response = self.request(weixin_requests=weixin_requests)
            try:
                print(response.status_code)
            except:
                pass
            if response and response.status_code in VALID_CODE:
                results = list(callback(response))
                if results:
                    for result in results:
                        print("new result")
                        if isinstance(result, WinxinRequests):
                            print("1 request added", type(result))
                            self.queue.add(result)
                        if isinstance(result, str):
                            print("\n\n\n1 page parsed")
                        else:
                            print(type(result))
                else:
                    self.error(weixin_requests)
            else:
                self.error(weixin_requests)

    def run(self):
        self.start()
        self.schedule()


a = Spider()
a.run()
