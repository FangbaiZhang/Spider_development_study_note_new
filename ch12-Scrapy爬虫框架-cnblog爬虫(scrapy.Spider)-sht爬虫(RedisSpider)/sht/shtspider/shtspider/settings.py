# -*- coding: utf-8 -*-

# Scrapy_工作原理_组件介绍 settings for shtspider project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'shtspider'

SPIDER_MODULES = ['shtspider.spiders']
NEWSPIDER_MODULE = 'shtspider.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'shtspider (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy_工作原理_组件介绍 (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
#}

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    'shtspider.middlewares.ShtspiderSpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'shtspider.middlewares.ShtspiderDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
ITEM_PIPELINES = {
    'scrapy_redis.pipelines.RedisPipeline':301, # scrapy-redis默认的pipeline，权限在自定义之后
    'shtspider.pipelines.ShtspiderPipeline': 300,
    'shtspider.pipelines.MyImagesPipeline': 1,

}

# ShtspiderPipeline用于下载ITEM中的文字数据到本地
# 上面添加了自定义的ImagesPipeline管道用于下载图片
# 设置图片的下载地址，图片地址，文件结果信息，并可制作大小缩略图
IMAGES_STORE = 'D:\Hello World\python_work\Spider_development_study_note\ch12\sht\shtimages'
IMAGES_URLS_FIELD = 'image_urls' # 下载图片的地址来源
IMAGES_REULT_FIELD = 'images'    # 图片文件的scrapy.Field()
IMAGES_THUMBS = {                # 设置要存储的缩略图大小，不写就是没有缩略图，只有原始大小图片
    'small': (50, 50),
    'big': (270, 270),
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy_工作原理_组件介绍 should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'

# 使用scrapy_redis的调度器，
# 启动爬虫前需要先CMD启动本地的redis-server，然后处于打开状态，然后再运行爬虫
# 第一遍运行后，已经爬取过的数据都会存储在redis数据库中，然后再次运行，由于都是爬取过的，爬虫会迅速结束，
# 有新的内容才会继续爬取
SCHEDULER = 'scrapy_redis.scheduler.Scheduler'
# （可选参数）数据是否持久化，程序停止数据保存，下次启动数据继续使用
# 在Redis中保持scrapy-redis用到的各个队列，从而允许暂停和暂停后恢复
SCHEDULER_PERSIST = True
# 使用scrapy_redis的指纹去重方式
DUPEFILTER_CLASS = 'scrapy_redis.dupefilter.RFPDupeFilter'
# 使用scrapy_redis的存储方式,见上面ITEM_PIPELINES，并将顺序设置成最后一个，用于存储下载所有的数据
# 定义Redis的IP和端口
REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


# 注意，改造成分布式爬虫后，传人URL，已经爬取过的ITEM会存储在本地服务器中
# 如果再次传入的网址，里面已经爬过的就直接过滤了，不会重复爬取，要想从头开始爬取，要删除redis中的相关数据
# 可以在redis中输入keys * 查看所有的键
# 使用del keyname 删除键及对应的值
# 127.0.0.1:6379> del sht:items          # 爬取到的item信息
# (integer) 1
# 127.0.0.1:6379> del sht:dupefilter     # 已爬取过的requests对象的指纹信息   sht:requests 待爬取的requests对象
# (integer) 1

# 使用flushall可以删除所有本地所有的键值数据
# 删除数据后再次传入起始URL，然后启动爬虫，就可以从原始状态开始爬取
# 注意：分布式爬虫，redis服务器一直处于运行状态，爬虫不会自己结束，
# 可以通过CMD窗口向服务器一直传入新的URL，然后爬虫会自动继续爬取新的URL，重复的会自动跳过
# 爬取完成后，手动结束爬虫程序即可


