# -*- coding: utf-8 -*-

# Scrapy settings for foodmate_scrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

#搜索条件
title = "芝麻油"

#footmate
#产品名称
kw = '芝麻油'
#判断结果 '1'-合格 '2'-不合格 ''全部
hege = ''
#不合格原因 '1'-质量指标 '2'-微生物 ''-请选择（全选）
xmfl1 = ''
#抽检级别 ''-全部 '1'-国抽 '2'-省抽
jibie = ''
#通报开始时间 '2015-01-12'
timebegin = '2021-04-01'
#通报结束时间
scrapy_end_time = '2021-04-02'
catidname = ''
page = 1
#一次的搜索周期，单位天
addDay = 1

#eshian
pageNo = "0"
#发布开始日期
releaseTime = "2015-12-30"
#发布结束日期
releaseTime1= "2021-04-16"
#产品名称
typeName= "芝麻油"
belowStandard= ""
brand= ""
#发布开始日期
releaseTimeX= "2015-12-30"
#发布结束日期
releaseTime1X= "2021-04-16"
brandX= ""
#产品名称
typeNameX= "芝麻油"
belowStandardX= ""
pTypeName= ""
pTypeId= ""
diquName= "全国"
diquId= "1"
#不合格分类
buhegeName= "污染物"
#21-感官 22-标签标识.... 26-污染物 27-农药残留 28-兽药残留
buhegeId= "26"
territories= "0"

BOT_NAME = 'foodmate_scrapy'

SPIDER_MODULES = ['foodmate_scrapy.spiders']
NEWSPIDER_MODULE = 'foodmate_scrapy.spiders'

# 设置item——pipelines
ITEM_PIPELINES = {
    'foodmate_scrapy.pipelines.FoodmateScrapyPipeline': 300,
}

# 设置请求头部，添加url
DEFAULT_REQUEST_HEADERS = {
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 '
                  + 'Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8'
}
# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'foodmate_scrapy (+http://www.yourdomain.com)'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://doc.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
DOWNLOAD_DELAY = 5
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
#    'foodmate_scrapy.middlewares.FoodmateScrapySpiderMiddleware': 543,
#}

# Enable or disable downloader middlewares
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#DOWNLOADER_MIDDLEWARES = {
#    'foodmate_scrapy.middlewares.FoodmateScrapyDownloaderMiddleware': 543,
#}

# Enable or disable extensions
# See https://doc.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    'scrapy.extensions.telnet.TelnetConsole': None,
#}

# Configure item pipelines
# See https://doc.scrapy.org/en/latest/topics/item-pipeline.html
#ITEM_PIPELINES = {
#    'foodmate_scrapy.pipelines.FoodmateScrapyPipeline': 300,
#}

# Enable and configure the AutoThrottle extension (disabled by default)
# See https://doc.scrapy.org/en/latest/topics/autothrottle.html
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
# See https://doc.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = 'httpcache'
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = 'scrapy.extensions.httpcache.FilesystemCacheStorage'
