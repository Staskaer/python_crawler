# 定义了与redis进行通信的类

from pickle import dumps, loads

from requests.api import request
from Requests_ import WinxinRequests
from redis import StrictRedis

from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import REDIS_KEY
from settings import REDIS_PASSWORD
from settings import REDIS_DB


class RedisQueue():
    def __init__(self):
        self.db = StrictRedis(host=REDIS_HOST, port=REDIS_PORT,
                              password=REDIS_PASSWORD, db=REDIS_DB)

    def add(self, requests):
        # 向队列中添加request对象
        if isinstance(requests, WinxinRequests):
            return self.db.rpush(REDIS_KEY, dumps(requests))
        return False

    def pop(self):
        if self.db.llen(REDIS_KEY):
            return loads(self.db.lpop(REDIS_KEY))
        else:
            return False

    def empty(self):
        return self.db.llen(REDIS_KEY) == 0
