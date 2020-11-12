# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

'''
# 以下代码为第一种方式：只获取帖子中的第一张图片，即电影的封面图片对应的代码
class ShtspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    url = scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
'''


# '''
# 以下代码为第二种方式：获取封面图片和内容截图
class ShtspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field() # 帖子标题
    content = scrapy.Field() # 帖子中种子的magnet值
    url = scrapy.Field() # 帖子的链接地址
    image_urls = scrapy.Field() # 一个帖子内所有图片的地址
    image_url_cover = scrapy.Field() # 电影封面图片的地址
    image_url_detail = scrapy.Field() # 电影内容截图的地址
    images = scrapy.Field() # 所有图片的item
    
# '''

