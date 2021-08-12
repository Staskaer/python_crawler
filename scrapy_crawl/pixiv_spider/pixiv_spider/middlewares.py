# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from time import sleep
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import scrapy
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class PixivSpiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class PixivSpiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        '''
        一开始想用selenium来模拟登录并将cookie导出到scrapy，但是selenium导出的cookie不全，只能放弃这种方法
        flag = request.meta.get('login', False)
        targeturl = request.meta.get('target', None)
        if flag and targeturl:

            browser = webdriver.Chrome()
            browser.get(request.url)
            button = browser.find_element_by_class_name(
                "signup-form__submit--login")
            button.click()
            username = browser.find_element_by_xpath(
                "//input[@autocomplete='username']")
            username.send_keys("")
            password = browser.find_element_by_xpath(
                "//input[@autocomplete='current-password']")
            password.send_keys("")
            button = browser.find_elements_by_xpath(
                "//button[@class = 'signup-form__submit']")[-1]
            button.click()
            sleep(1)

            cookies = browser.get_cookies()
            print(cookies, '\n\n')
            temp = {}
            for cookie in cookies:
                temp[cookie['name']] = cookie['value']
            browser.quit()
            print(temp)
            print('\n')
            print(targeturl)
            print('\n')

            cookies = {'first_visit_datetime_pc': '2021-08-11+20%3A49%3A14', ' p_ab_id': '8', ' p_ab_id_2': '4', ' p_ab_d_id': '2052193440', ' yuid_b': 'FUgnd0U', ' PHPSESSID': '43205537_VyORHjQqPcLYb9AVsw4YPSZ9q8HVwack', ' device_token': 'd2055b3efcc40de9dad47f13286c2f58', ' privacy_policy_agreement': '3', ' c_type': '30',
                       ' privacy_policy_notification': '0', ' a_type': '0', ' b_type': '1', ' __cf_bm': '8b79883794bb4d40b1c92400bc988d1221714439-1628684977-1800-AW1OZCo7k9euuLsJopuK8Ppa7Et8XibaJVuzQCtx0UwzfyGovh0VBYFHmC8XFNLXDGyM5kXy1l8N/Mf58I6mHRW6r2K3P2SQBw/T9ohhse9Uw3uaUpENI/nG+jtx6fLTmWjCP/Rt9cbNpbISqiDipOeIGgq9GdJ3K8vTKryNgdnSuFtnSCJ3BV1EjH3mANW0DA=='}
            print(cookies)
            cookies = None
            return scrapy.Request(url=targeturl, cookies=cookies, meta={'login': False})
            '''
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
