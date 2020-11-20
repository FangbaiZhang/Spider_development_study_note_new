# -*- coding: utf-8 -*-
# 一个福利网站资源爬取

# 使用说明：
# 1. 修改该代码文件中allowed_domains和page_url为有效的域名
# 2. 爬虫启动在CMD窗口中进行，具体参考下面说明
# 3. 种子连接下载后会自动生成一个json文件保存在该项目目录下，json文件转为为word文件，查看ch00中实例
# 4. 下载的图片以帖子标题命名保存在shtimages文件夹目录下
# 5. 分布式爬虫爬取过的会自动过滤，完成一次全新爬取，需要删除本地键值，具体查看改代码末尾说明

# 由于网站经常更换域名，爬虫会很快失效
# 再次爬取时候需要检查修改2处：allowed_domains和page_url将其更换为正确的网址
# 下面注释中还有https://www.dsndsht23.com/，是之前的域名，已经失效

# 注意sht是我手动创建的文件夹，shtspider文件夹才是爬虫项目主文件夹

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
    # 修改地方1：主域名要检查更改为新的有效域名
    allowed_domains = ['98zudisw.xyz']

    # 推荐使用以下方式1：
    # 网站更新后，只需要爬取固定的某几页，可以将要爬取的页面放到开始网址中，lpush要爬取的页面，可以一次编辑好命令后传进去
    # 直接复制首页，后面几页就是URL中一个数字的变化
    # 然后注释掉下面爬取下一页的功能，就只会爬取开始列表中的几页，redis里面直接

    # 方式2：(适用于主域名还没有变化的情况)
    # 备注：由于本地redis中已经缓存了爬取的内容，包含网址和item内容
    # 也可以直接用论坛第一页爬取整个论坛，以前爬过的自动跳过，但是域名会不断更新，导致每个帖子地址也发生了变化，
    # 虽然redis中缓存了url和item信息，但是之前的信息，是否又全部爬取一遍，有待验证？
    # 或者在每一页时候，判断一下帖子日期(将日期数字提取拼接成数字，然后判断大小)，
    # 帖子顶部有发帖日期，解析帖子详细内容时候，先判断日期，日期前的跳过，日期后的提取详细内容

    # redis爬虫也可以只爬取某几页，还是注释掉下面的start_urls，然后要注释掉爬取下一页的代码，
    # 然后lpush sht:start_urls 中依次传入要爬取的那几个网址即可，比如只爬取第一页，第二页、、、、，可以一次传入多个

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
    # 可以在redis-cli一次性传入多个，这样就一次全部爬取了，但是这样就全部写入一个json文件了,
    # 可以爬取完一个分论坛再爬取下一个分论坛，先停止爬虫，将管中将json文件重新命名后或者直接重命名已经爬取到的json文件都可以，然后再爬取下个url
    # 127.0.0.1:6379> lpush sht:start_urls https://www.dsndsht23.com/forum-103-1.html （高清中文字幕首页爬取的键值）
    # lpush sht:start_urls https://www.dsndsht23.com/forum-2-1.html  （国产原创）
    # 现在redis-cli里面传入上面网址（成功后显示(integer) 1），然后右键run启动运行主爬虫程序sht_spider.py，爬取就开始了
    # 一个网址爬取结束后，向里面再次传入新的URL就可以继续爬取，设置键的名称，键的值启动爬虫后CMD中输入
    # 由于该网址是国外域名，可能开始请求几次会出现失败，爬虫自己会尝试不断请求，过一会儿就会成功
    # 启动后要等待1分钟左右，可能更长，才会大量开始爬取
    # redis爬虫键的名称。值就是初始URL
    redis_key = 'sht:start_urls'

    def parse(self, response):
        # 网页主域名（网站首页），用于后面网址的拼接
        # 修改地方2：主页域名爬取要进行检查修改为新的主域名
        page_url = 'https://www.98zudisw.xyz/'
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        # 先获取一页下面所有的帖子的标签
        papers = soup.find_all('a', class_="s xst", href=re.compile(r'thread-.*'))
        for paper in papers:
            old_url = paper['href']
            # 解析出来的url是一个字符串, 检查网页源代码看到的url有所变化，需要拼接上网站主域名，才是真正的网址
            # 可以用urljoin函数拼接，也直接可以用字符串相加拼接
            # full_url = 'https://www.dsndsht23.com/' + url
            url = urljoin(page_url, old_url)
            # full_url = 'https://www.dsndsht23.com/' + url
            # paper标签里面的text内容就是帖子标题
            title = paper.get_text()
            # 将帖子链接地址和标题传递给item
            item = ShtspiderItem(url=url, title=title)
            # 定义一个request，用于解析每一个帖子详细内容，同时传递item
            request = scrapy.Request(url=url, meta={'item': item}, callback=self.parse_body)
            # 使用生成器yield，循环请求
            yield request


        # 爬取下一页的内容,如果只需要爬取某一页，就将下面寻找爬取下一页代码注释掉即可
        # '''
        next_page = soup.find('a', class_="nxt")
        next_page_url = page_url + next_page['href']
        try:
            if next_page:
                # 如果有下一页的地址，下一页继续调用parse方法进行解析
                yield scrapy.Request(url=next_page_url, callback=self.parse)
        except Exception:
            print("所有主页面爬取结束！")
        # '''

    '''
    # 注意：只获取封面图片，即第一张图片，是最初代码，后期添加了爬取封面图片和内如图片代码
    # 代码切换说明：需要将sht_spider/pipelines/items.py三个文件中代码进行交叉注释，
    # 其它不动，要不使用第一种方式，要不只使用第二种方式，item设置和内容不同，图片管道不同
    # 进入一个帖子里面，获取里面的内容
    # 以下代码为第一种方式：只获取帖子中的第一张图片，即电影的封面图片
    def parse_body(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        try:
            # 获取封面图片，find只匹配到第一个标签就结束了，zoom有两个结果，第二个是内容截图
            image_url = soup.find('img', class_='zoom')
            magnet = soup.find('div', class_='blockcode').find('li')
            # 提取出图片的地址和magnet值
            image_urls = image_url['file']
            content = magnet.string
            item['image_urls'] = image_urls
            item['content'] = content
            yield item
        except Exception:
            print("所有分页面爬取结束！")
    '''


    # '''
    # 进入一个帖子里面，获取里面的内容
    # 以下代码为第二种方式：获取帖子中的第一张图片和第二张图片，提取出来，如果有更多图片，需要继续修改代码，但是只需要前两张图片即可
    def parse_body(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
        try:
            # 图片中包含一张封面图，一张内容图，class属性都是zoom
            image_urls = []
            image_urls_tag = soup.find_all('img', class_='zoom')
            # 如果有大量的图片，可以先找出所有，然后for循环取出，
            # append添加到image_urls/列表中去，管道里面下载方法一样，循环取出列表，每个图片都会下载下来
            # 图片重命名时候，使用标题名称创建文件夹即可，每个帖子的图片都下载在一个单独文件夹中
            magnet = soup.find('div', class_='blockcode').find('li')
            # 提取出图片的地址(使用列表方法取出元素)和magnet值，标签中的file属性的值就是图片的网址
            image_url_cover = image_urls_tag[0]['file']
            image_url_detail = image_urls_tag[1]['file']
            content = magnet.string # 字符串就是magnet值
            image_urls.append(image_url_cover)
            image_urls.append(image_url_detail)

            # 将上面提取到的所有内容传递给item
            item['image_urls'] = image_urls
            item['image_url_cover'] = image_url_cover
            item['image_url_detail'] = image_url_detail
            item['content'] = content
            # 使用生成器，循环生成item
            yield item

        except Exception:
            print("所有分页面爬取结束！")
    # '''

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
# 使用del keyname 删除键及对应的值,删除所有sht相关的键值，不然开始爬取会没有内容，因为items爬取存储过了
# 127.0.0.1:6379> del sht:items
# (integer) 1
# 127.0.0.1:6379> del sht:dupefilter
# (integer) 1
# 127.0.0.1:6379> del sht:start_urls
# (integer) 1
# 127.0.0.1:6379> del sht:requests
# (integer) 1

# 然后传入起始网址，启动运行爬虫
# 127.0.0.1:6379> lpush sht:start_urls https://www.98zudisw.xyz/forum-103-1.html

# 使用flushall可以删除所有本地所有的键值数据
# 删除数据后再次传入起始URL，然后启动爬虫，就可以从原始状态开始爬取
# 注意：分布式爬虫，redis服务器一直处于运行状态，爬虫不会自己结束，
# 可以通过CMD窗口向服务器一直传入新的URL，然后爬虫会自动继续爬取新的URL，重复的会自动跳过
# 爬取完成后，手动结束爬虫程序即可
# 注意：爬取的图片放在ch12文件夹的sht_spider.py同目录文件夹里面

