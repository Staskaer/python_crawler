# 这个文件配置了重要的参数

# save_文件使用到的

# 最大分数
MAX_SCORE = 100
# redis存储中可以存在的最小分数（不包含）
MIN_SCORE = 0
# 每次测试不通过的扣分数
DECREASE_POINT = 5
# 爬虫抓取到的代理的初始分数
INITIAL_SCORE = 10
# redis主机
REDIS_HOST = 'localhost'
# redis端口
REDIS_PORT = 6379
# redis密码
REDIS_PASSWORD = '123456'
# redis键名
REDIS_KEY = 'proxies'


# spider_文件使用到的


# testproxy文件使用到的

# 合法的返回码
VALID_STATUS_CODE = [200]
# 测试链接
TEST_URL = "http://www.baidu.com"
# 最大同时测试数目
BATCH_TEST_SIZE = 40
# 测试的超时时间
TEST_TIMEOUT = 15

# getter文件使用到的

# 存储的代理的最多数目
POOL_MAX_SAVE_COUNTS = 1000


# dispatch文件使用到的

# 测试结束后停止多久开始下一轮测试
TEST_CYCLE = 20
# 抓取结束后停止多久开始下一轮抓取
GETTER_CYCLE = 180
# 测试模块的开关
TEST_ENABLE = True
# 抓取模块开关
GETTER_ENABLE = True
# api模块开关
API_ENABLE = True
# api主机
API_HOST = '127.0.0.1'
# api端口
API_PORT = 5555
