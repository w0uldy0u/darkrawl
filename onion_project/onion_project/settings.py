# Scrapy settings for onion_project project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "onion_project"

SPIDER_MODULES = ["onion_project.spiders"]
NEWSPIDER_MODULE = "onion_project.spiders"

ADDONS = {}


HTTPPROXY_ENABLED = True

# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = ""

# Obey robots.txt rules
ROBOTSTXT_OBEY = False
DEFAULT_REQUEST_HEADERS = {
    "Cookie": "__RequestVerificationToken=fVqMp1otO8XvjsYovQAVfoVpABDVWzTQcCSQ7hp7pdMUU7NUCKIe5JjAIr7DC95FSulBi7BUihfrAlpG37cUsrHH_3PqDtp2eBXfyQu5b6A1; .ASPXAUTH=AB63D579AFEEC8ED4A4BC6A5B4681F0DA1C9DFFA62DF60FCB6C158D6BEF78F1994B9641569B1D85D18A86061240A0E7A00073837A04DCD7B432AF3512B01FC5B8959F1C93424C149DC143DCFBD73F8222F2434B6F229BCFFC732F18114AB7340B6B456112F0220EDB7CB2A2472F1ED1F41C686B0882DEA82269B8A1BC1CE6038"
}
# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "onion_project.middlewares.OnionProjectSpiderMiddleware": 543,
#}

# Enable or disable downloader middlewares
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
DOWNLOADER_MIDDLEWARES = {
#    "onion_project.middlewares.OnionProjectDownloaderMiddleware": 543,
     "scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware": 110,
     'onion_project.middlewares.ForceProxyMiddleware': 100,
}

# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

# Configure item pipelines
# See https://docs.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    "onion_project.pipelines.OnionProjectPipeline": 300,
#}

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
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
