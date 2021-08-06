# 为获取模块提供存储类

from random import choice
import redis

from settings import MAX_SCORE
from settings import MIN_SCORE
from settings import DECREASE_POINT
from settings import INITIAL_SCORE
from settings import REDIS_HOST
from settings import REDIS_PORT
from settings import REDIS_PASSWORD
from settings import REDIS_KEY


class RedisClient(object):
    def __init__(self, host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD):
        self.db = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True)

    def add(self, proxy, score=INITIAL_SCORE):
        # 此方法用于添加新的可用代理，分数为初始化分数
        if not self.db.zscore(REDIS_KEY, proxy):
            zmap = {
                proxy: score
            }
            return self.db.zadd(REDIS_KEY, zmap)

    def random(self):
        # 此方法用于随机从可用代理中选出一个，默认最高分
        # 当不存在最高分时将从前10位中随机选择一个
        result = self.db.zrangebyscore(REDIS_KEY, MAX_SCORE, MAX_SCORE)
        if len(result):
            return choice(result)
        else:
            result = self.db.zrevrange(REDIS_KEY, 0, 10)
            if len(result):
                return choice(result)
            else:
                return None

    def decrease(self, proxy):
        # 将不可用代理分数减去定义的数值，到0则移除
        score = self.db.zscore(REDIS_KEY, proxy)
        if score and score > MIN_SCORE:
            print('代理', proxy, '当前分数', score, '减{}，变为'.format(
                DECREASE_POINT), score - DECREASE_POINT)
            score = score - DECREASE_POINT
            if score <= MIN_SCORE:
                print("代理", proxy, '移除')
                return self.db.zrem(REDIS_KEY, proxy)
            mapping = {
                proxy: score,
            }
            return self.db.zadd(REDIS_KEY, mapping)
        else:
            print("代理", proxy,  '移除')
            return self.db.zrem(REDIS_KEY, proxy)

    def exist(self, proxy):
        # 判断某代理是否存在
        return not self.db.zscore(REDIS_KEY, proxy) == None

    def max(self, proxy):
        # 将某代理设置为最大分数
        print("代理", proxy, "可用，设置为", MAX_SCORE)
        mapping = {
            proxy: MAX_SCORE,
        }
        self.db.zadd(REDIS_KEY, mapping)

    def count(self):
        # 返回代理总数
        return self.db.zcard(REDIS_KEY)

    def all(self):
        # 返回全部代理
        return self.db.zrangebyscore(REDIS_KEY, MIN_SCORE, MAX_SCORE)
