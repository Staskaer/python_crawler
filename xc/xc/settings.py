# Scrapy settings for xc project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'xc'

SPIDER_MODULES = ['xc.spiders']
NEWSPIDER_MODULE = 'xc.spiders'

# LOG_LEVEL = "WARNING"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'xc (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 0.5
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'xc.middlewares.XcSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'xc.middlewares.XcDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'xc.pipelines.XcPipeline': 300,
}


SQL_HOST = "127.0.0.1"
SQL_USR = "root"
SQL_PASSWORD = "root"
SQL_DB = "xiecheng"
SQL_PORT = 3306
# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

PAGE = 1
json_data = {
    'arg': {
        'channelType': 2,
        'collapseType': 0,
        'commentTagId': 0,
        'pageIndex': 1,
        'pageSize': 10,
        'poiId': 13412802,
        'sourceType': 1,
        'sortType': 3,
        'starType': 0,
    },
    'head': {
        'cid': '09031083117409368977',
        'ctok': '',
        'cver': '1.0',
        'lang': '01',
        'sid': '8888',
        'syscode': '09',
        'auth': '',
        'xsid': '',
        'extension': [],
    },
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    # Requests sorts cookies= alphabetically
    # 'Cookie': 'Union=AllianceID=4897&SID=130026&OUID=&createtime=1653640960&Expires=1654245760240; GUID=09031083117409368977; _RF1=112.32.53.220; _RSG=UF4Ii.zwS9EjRO1i.tc7R8; _RDG=288d1c5e0a588d29fb16bb7bc8b5e248ca; _RGUID=e25cebdf-ac48-43de-86c7-9b7fac0586ed; _bfaStatusPVSend=1; MKT_CKID_LMT=1653640965310; MKT_CKID=1653640965310.3y6nd.ld63; Session=SmartLinkCode=zhihu&SmartLinkKeyWord=&SmartLinkQuary=_UTF.&SmartLinkHost=link.zhihu.com&SmartLinkLanguage=zh; StartCity_Pkg=PkgStartCity=30; nfes_isSupportWebP=1; _bfaStatus=fail; _bfa=1.1653640960531.60r5i.1.1653640960531.1653640960531.1.11.1; _bfs=1.11; _ubtstatus=%7B%22vid%22%3A%221653640960531.60r5i%22%2C%22sid%22%3A1%2C%22pvid%22%3A11%2C%22pid%22%3A0%7D; _bfi=p1%3D290510%26p2%3D0%26v1%3D11%26v2%3D0; __zpspc=9.1.1653640965.1653641337.7%234%7C%7C%7C%7C%7C%23; _jzqco=%7C%7C%7C%7C%7C1.189451031.1653640965324.1653641277352.1653641337815.1653641277352.1653641337815.0.0.0.7.7',
    'Origin': 'https://you.ctrip.com',
    'Pragma': 'no-cache',
    'Referer': 'https://you.ctrip.com/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36',
    # Already added when you pass json=
    # 'content-type': 'application/json',
    'cookieOrigin': 'https://you.ctrip.com',
    'dnt': '1',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="101", "Google Chrome";v="101"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-gpc': '1',
}
