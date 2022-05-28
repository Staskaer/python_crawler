# Scrapy settings for pixiv_spider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'pixiv_spider'

SPIDER_MODULES = ['pixiv_spider.spiders']
NEWSPIDER_MODULE = 'pixiv_spider.spiders'

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36"

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'pixiv_spider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
LOG_LEVEL = 'WARNING'

COOKIES = 'first_visit_datetime_pc=2022-01-31+23%3A58%3A31; yuid_b=FVaQWYg; p_ab_id=5; p_ab_id_2=2; p_ab_d_id=502202489; PHPSESSID=43205537_umMBLnM1PKFEvslolEKQtJL1uzlkEQKf; device_token=f87bf77055b887485f7aa7c3e846e855; privacy_policy_agreement=3; c_type=31; privacy_policy_notification=0; a_type=0; b_type=1; __cf_bm=ywBY9zAJ_sxmH7efkaIeims1nnHdtOLiGRxR4E28ffg-1644330267-0-AR15NeetheUMcJbCRx6pi4tdSOhIz7kK2rBO119aklK8CF3d5hmr4GbbgRLD6dhO26OqUMpBpqUDGiPaw1VywflL1Dh/xELRnYr7d1ZR4YwFM+7erdktUu74gWcDh/jnFWmFDr6y1T5xSuPUznR3k0Gq4PdTjm7mRgfYGTgCpCkZpcoyjJCZ7PSjTPLkhoJzNA==; tag_view_ranking=zIv0cf5VVk~0xsDLqCEW6~V3EerOWlfp~NPZqX59qdv~-0JKThjl-M~bMvAR_D5Tw~_74SH24rqw~PBGiE_ppDD~tTvZK72fmv~Lp6pHlVTm8~Ce-EdaHA-3~1Gs7WPT7fK~34EpeNsQw1~HjkJl241ME~ko30YJxw7F~Y04kSN8Q7d~O0WKFZuVbs~y8GNntYHsi~BU9SQkS-zU~8Qlpl5et8m~RcahSSzeRf~ePN3h1AXKX~48VvbTaVxS~-pq5Nu4OQE~FqVQndhufZ~UE6jCSAq4S~-StjcwdYwv~-L-4bBqjrT~rezgCfkPbs~FqEilr4cQe~m35RGtcHc_~Dy92A-d4Nq~f7A2Tb8_HR~h7fLeUgfMX~t7gAIsgQW9~PwDMGzD6xn~I-8NIYNueU~QtDSenXBgu; QSI_S_ZN_5hF4My7Ad6VNNAi=r:10:15'
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

IMAGES_STORE = './arcaea'
# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'pixiv_spider.middlewares.PixivSpiderSpiderMiddleware': 543,
# }

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
# DOWNLOADER_MIDDLEWARES = {
#    'pixiv_spider.middlewares.PixivSpiderDownloaderMiddleware': 543,
# }

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
# EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
# }

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'pixiv_spider.pipelines.PixivSpiderPipeline': 300,
}

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
