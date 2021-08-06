# 获取模块，定义了获取器类
# 此模块调用spider中的额爬取模块来获取代理
# 并调用redisclient来存入redis中

from time import sleep
from save_ import RedisClient
from spider_ import Crawler

from settings import POOL_MAX_SAVE_COUNTS


class Getter(object):
    def __init__(self):
        self.redis = RedisClient()
        self.crawl = Crawler()

    def is_over_count(self):
        # 检测代理池是否达到上限
        if self.redis.count() >= POOL_MAX_SAVE_COUNTS:
            return True
        else:
            return False

    def run(self):
        # 遍历__CrawlFunc__中的由元类定义的所有爬取函数
        # 实现爬存功能
        if not self.is_over_count():
            for callback_label in range(self.crawl.__CrawlCount__):
                callback = self.crawl.__CrawlFunc__[callback_label]
                try:
                    proxies = self.crawl.get_proxies(callback=callback)
                    for proxy in proxies:
                        self.redis.add(proxy=proxy)
                except:  # 当失败后会重新尝试获取代理，但只会重试一次
                    print("获取失败，准备重试...")
                    sleep(2)
                    try:
                        proxies = self.crawl.get_proxies(callback=callback)
                        for proxy in proxies:
                            self.redis.add(proxy=proxy)
                    except:
                        print("重新获取失败，不再重试，等待下一轮循环...")
