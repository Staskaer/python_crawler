# 这个文件配置了重要的参数

# save_文件使用到的

# 最大分数
MAX_SCORE = 100
# redis存储中可以存在的最小分数（不包含）
MIN_SCORE = 0
# 每次测试不通过的扣分数
DECREASE_POINT = 5
# 满分代理扣除的分数
DECREASE_MAX_POINT = 1
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
TEST_URL = "http://www.baidu.com/"
# 说明：由于aiohttp异步请求库不支持https代理，所以此处应该使用http协议
# 默认配置下采集到的代理均支持https代理，所以从api获取到的代理均可以使用https请求

# 最大同时测试数目
BATCH_TEST_SIZE = 40
# 测试的超时时间
TEST_TIMEOUT = 10
# 满分代理的测试超时时间
MAX_TEST_TIMEOUT = 7

# getter文件使用到的

# 存储的代理的最多数目
POOL_MAX_SAVE_COUNTS = 1000


# dispatch文件使用到的

# 测试结束后停止多久开始下一轮测试
TEST_CYCLE = 20
# 抓取结束后停止多久开始下一轮抓取
GETTER_CYCLE = 180
# 满分测试模块的周期
MAX_SCORE_CYCLE = 5
# 测试模块的开关
TEST_ENABLE = True
# 抓取模块开关
GETTER_ENABLE = True
# api模块开关
API_ENABLE = True
# 满分检测模块
MAX_SCORE_ENABLE = True
# api主机
API_HOST = '127.0.0.1'
# api端口
API_PORT = 5555
