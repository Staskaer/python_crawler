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

COOKIES = 'yuid_b=IyEQQ0M; first_visit_datetime_pc=2021-08-11+22%3A16%3A52; p_ab_id=7; p_ab_id_2=8; p_ab_d_id=941474410; __cf_bm=6bc13a615e935d3c9a4e8e80dbad4f7fc481d89a-1628687814-1800-AToUl/+XMRg0nDQRaiqMj4l9fASZL1rOdfGFkaySexX/CstoIoTmJFPfxc1L8FKo9rvESje3A/ml3UffAcFTnm16vPXxXerz2DkwAYEKZRefHWT7AtUUK5GXg+cBLEwCbe4iwLByTdIwjJDc1IXPcZ89n07zWCWHxe+NyfYnH4B1atq/aJenWwBvdQdh79zDgg==; PHPSESSID=43205537_RrV6koOz9r7dhUPkWzelRglBaW71Fox2; device_token=0c743420076cdc0a2a1ec79cc7ec5227; privacy_policy_agreement=3; c_type=30; privacy_policy_notification=0; a_type=0; b_type=1'
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
