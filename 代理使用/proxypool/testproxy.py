# 这是用于检测代理可用性的模块

from save_ import RedisClient
import aiohttp
import asyncio
from time import sleep

from settings import VALID_STATUS_CODE
from settings import TEST_URL
from settings import BATCH_TEST_SIZE
from settings import TEST_TIMEOUT
from settings import MAX_TEST_TIMEOUT


class Tester(object):
    def __init__(self):
        self.redis = RedisClient()

    async def test_single_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = "http://"+proxy
                print("正在测试", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=TEST_TIMEOUT) as response:
                    if response.status in VALID_STATUS_CODE:
                        self.redis.max(proxy)
                        print("代理可用", proxy)
                    else:
                        self.redis.decrease(proxy)
                        print("请求响应码{}不合法".format(response.status), proxy)
            except:
                self.redis.decrease(proxy)
                print("代理请求失败", proxy)

    def run(self):
        try:
            proxies = self.redis.all()
            loop = asyncio.get_event_loop()
            for i in range(0, len(proxies), BATCH_TEST_SIZE):
                test_proxies = proxies[i:i+BATCH_TEST_SIZE]
                tasks = [self.test_single_proxy(proxy)
                         for proxy in test_proxies]
                loop.run_until_complete(asyncio.wait(tasks))
                sleep(5)
        except:
            print("测试器发生错误")


class Test_max_score(object):
    # 这个模块检验所有满分代理
    def __init__(self):
        self.redis = RedisClient()

    async def test_max_score_proxy(self, proxy):
        conn = aiohttp.TCPConnector(verify_ssl=False)
        async with aiohttp.ClientSession(connector=conn) as session:
            try:
                if isinstance(proxy, bytes):
                    proxy = proxy.decode('utf-8')
                real_proxy = "http://"+proxy
                print("正在测试满分代理", proxy)
                async with session.get(TEST_URL, proxy=real_proxy, timeout=MAX_TEST_TIMEOUT) as response:
                    if response.status in VALID_STATUS_CODE:
                        print("满分代理可用，保留", proxy)
                    else:
                        self.redis.decrease_max(proxy)
                        print("满分代理请求响应码{}不合法".format(response.status), proxy)
            except:
                self.redis.decrease_max(proxy)
                print("满分代理请求失败", proxy)

    def run(self):
        try:
            proxies = self.redis.max_score()
            loop = asyncio.get_event_loop()
            test_proxies = proxies
            tasks = [self.test_max_score_proxy(proxy)
                     for proxy in test_proxies]
            loop.run_until_complete(asyncio.wait(tasks))
            sleep(5)
        except:
            print("满分测试器发生错误")
