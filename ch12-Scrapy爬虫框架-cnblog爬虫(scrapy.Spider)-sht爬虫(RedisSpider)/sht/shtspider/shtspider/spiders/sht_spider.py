# -*- coding: utf-8 -*-
# 一个福利网站资源爬取

# 由于网站经常更换域名，爬虫会很快失效
# 再次爬取时候需要检查allowed_domains和page_url将其更换为正确的网址
# 下面注释中还有https://www.dsndsht23.com/，是之前的域名，已经失效

# 注意sht是我手动创建的文件夹，shtspider才是爬虫项目主文件夹

import scrapy
import re
from urllib.parse import urljoin
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from bs4 import BeautifulSoup
from shtspider.items import ShtspiderItem

# 打造分布式爬虫
from scrapy_redis.spiders import RedisSpider


# 最原始的scrapy爬虫
# class ShtSpider(scrapy.Spider):

# 下面已经改造为redis去重爬虫，如果要使用手动输入的start_urls列表爬取，类还是继承scrapy.Spider
# 上面class ShtSpider(scrapy.Spider)注释和下面的start_urls的注释去掉
# 然后将下面的class ShtSpider(RedisSpider)和redis_key = 'sht:start_urls'注释掉
# 设置里面注释掉redis相关设置就恢复了最初的爬虫，但是不推荐，推荐使用redis爬虫


class ShtSpider(RedisSpider):
    name = 'sht'
    # 修改1：主域名要检查更改
    allowed_domains = ['sdfasf.space']

    # 网站更新后，只需要爬取固定的某几页，可以将要爬取的页面放到开始网址中，
    # 然后注释掉下面爬取下一页的功能，就只会爬取开始列表中的几页

    '''
    start_urls = [
        'https://www.200sht.info/forum-103-1.html',
        'https://www.200sht.info/forum-104-1.html',
    ]
    '''

    # RedisSpider不需要上面的start_urls，要用redis就直接注释掉，需要设置一个键的名称
    # 先打开一个CMD窗口，启动本地的redis-server，然后处于打开状状态
    # 打开CMD窗口，输入redis-cli连接到本地的redis-server
    # 或者直接WIN+R中运行redis-cli
    # 设置起始URL的键和值，爬虫中只需设置键的名称，然后进入CMD窗口输入键和值，值就是起始URL
    # 可以在redis-cli一次性传入多个，这样就一次全部爬取了，但是这样就全部写入一个json文件了,可以爬取完成后再爬取下一次，管道中将json文件重新命名
    # 127.0.0.1:6379> lpush sht:start_urls https://www.dsndsht23.com/forum-103-1.html （高清中文字幕爬取的键值）
    # lpush sht:start_urls https://www.dsndsht23.com/forum-2-1.html  （国产原创）
    # lpush sht:start_urls https://www.dsndsht23.com/forum-107-1.html  （三级写真）
    # 现在redis-cli里面传入上面网址（成功后显示(integer) 1），然后启动主爬虫程序，爬取就开始了
    # 一个网址爬取结束后，向里面再次传入新的URL就可以继续爬取，设置键的名称，键的值启动爬虫后CMD中输入
    # 由于该网址是国外域名，可能开始请求几次会出现失败，爬虫自己会尝试不断请求，过一会儿就会成功
    # 启动后要等待1分钟左右，可能更长，才会大量开始爬取
    # redis爬虫键的名称。值就是初始URL
    redis_key = 'sht:start_urls'


    def parse(self, response):
        # 网页主域名（网站首页），用于后面网址的拼接
        # 修改2：主页域名爬取要进行检查更新
        page_url = 'https://www.sdfasf.space/'
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        papers = soup.find_all('a', class_="s xst", href=re.compile(r'thread-.*'))
        for paper in papers:
            old_url = paper['href']
            # 解析出来的url是一个字符串和检查网页源代码看到的url有所变化，需要拼接上网站主域名，才是真正的网址
            # 可以用urljoin函数拼接，也直接可以用字符串相加拼接
            # full_url = 'https://www.dsndsht23.com/' + url
            url = urljoin(page_url, old_url)
            # full_url = 'https://www.dsndsht23.com/' + url
            title = paper.get_text()
            item = ShtspiderItem(url=url, title=title)
            request = scrapy.Request(url=url, meta={'item': item}, callback=self.parse_body)
            yield request

        # 爬取下一页
        next_page = soup.find('a', class_="nxt")
        next_page_url = page_url + next_page['href']
        try:
            if next_page:
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        except Exception:
            print("所有主页面爬取结束！")


    def parse_body(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        try:
            image_url = soup.find('img', class_='zoom')
            magnet = soup.find('div', class_='blockcode').find('li')
            # 提取出图片的地址和magnet值，标签中的file属性对应的值就是图片的网址
            image_urls = image_url['file']
            content = magnet.string # 字符串就是magnet值
            item['image_urls'] = image_urls
            item['content'] = content
            yield item
        except Exception:
            print("所有分页面爬取结束！")

# 命令行可以启动爬虫，我们也可以添加爬虫启动程序process，使用以下三行代码启动爬虫
# 启动主程序，干货都来了
# redis爬虫，先启动redis，传入要爬取的网址后再启动爬虫主程序(也可以启动爬虫后再传入网址，redis会等待传入键值)
# 启动后要等待1分钟左右，可能更长，才会大量开始爬取
if __name__ == '__main__':
    process = CrawlerProcess(get_project_settings())
    process.crawl('sht')
    process.start()

# 注意，改造成分布式爬虫后，传人URL，已经爬取过的ITEM会存储在本地服务器中
# 如果再次传入的网址，里面已经爬过的就直接过滤了，不会重复爬取，要想从头开始爬取，要删除redis中的相关数据
# 可以在redis中输入keys * 查看所有的键：127.0.0.1:6379> keys *
# 使用del keyname 删除键及对应的值
# 127.0.0.1:6379> del sht:items
# (integer) 1
# 127.0.0.1:6379> del sht:dupefilter
# (integer) 1

# 使用flushall可以删除所有本地所有的键值数据
# 删除数据后再次传入起始URL，然后启动爬虫，就可以从原始状态开始爬取
# 注意：分布式爬虫，redis服务器一直处于运行状态，爬虫不会自己结束，
# 可以通过CMD窗口向服务器一直传入新的URL，然后爬虫会自动继续爬取新的URL，重复的会自动跳过
# 爬取完成后，手动结束爬虫程序即可
# 注意：爬取的图片放在ch12文件夹里面

