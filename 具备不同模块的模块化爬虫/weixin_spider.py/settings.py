# 定义了一系列爬虫用到的重要参数

# Requests文件

# 超时时间
TIMEOUT = 10


# RedisQueue文件

# redis主机
REDIS_HOST = 'localhost'
# redis端口
REDIS_PORT = 6379
# redis密码
REDIS_PASSWORD = '123456'
# redis键名
REDIS_KEY = 'WeixinRequests'
# redis存储库
REDIS_DB = 0

# spider文件

# api接口
API_ADDRESS = 'http://127.0.0.1:5555/random'
# 最大重试次数
MAX_FAILED_TIMES = 5
# 合法状态码
VALID_CODE = [200, 302]
