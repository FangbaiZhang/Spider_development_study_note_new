# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import scrapy
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class ShtspiderPipeline(object):

    def __init__(self):
        self.file = open('papers.json', 'w', encoding='utf-8')

    # 将ITEM里面的信息写入到一个json文件中
    # json文件自动存储在sht_spider.py同一个文件夹中
    def process_item(self, item, spider):
        # 判断item字典对象中title对应的是否还有值
        if item['title']:
            # 将item字典类型的数据转换成json格式的字符串,
            # 注意json.dumps序列化时对中文默认使用的ascii编码，要想写入中文，加上ensure_ascii=False
            line = json.dumps(dict(item), ensure_ascii=False) + "\n"
            self.file.write(line)
            print("正在存储内容： " + item['title'])
            return item
        else:
            raise DropItem("Missing title in %s" % item)

'''
# 以下代码为第一种方式：只获取封面图片
class MyImagesPipeline(ImagesPipeline):

    # 获取图片的url,然后下载图片，因为每个帖子我们只提取了一个图片的地址，所以可以不用循环，直接使用下面Request请求下载
    # 注意，yield的请求里面一定要传入meta={'item': item}，
    # 请求时候才能从item中先获取image_urls列表，然后取出image_url，参数遗漏不能下载图片到本地，
    def get_media_requests(self, item, info):
        # for image_url in item['image_urls']:
        print("正在下载图片： " + item['title'])
        yield scrapy.Request(item['image_urls'], meta={'item': item})

    # 确认图片是否下载完成或者没有下载
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item

    # 图片重命名,重命名的名称就是存储的地址，只有一张图片，直接重命名
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        file_name = u'full/{}-{}.jpg'.format(item['title'], request.url.split("/")[-1])
        # file_name = u'full/{}.jpg'.format(item['title'])
        return file_name
'''


# '''

# 以下代码为第二种方式：获取封面图片和内容图片
# 定义标准的图片下载管道，通用方法，其它爬虫直接复制过去，注意settings.py中要设置存储图片的位置以及缩略图大小
class MyImagesPipeline(ImagesPipeline):

    # 获取图片的url,然后下载图片，scrapy.Request会根据图片url自动请求获取图片数据下载图片到设置的文件夹中
    # 注意，yield的请求里面一定要传入meta={'item': item}，
    # 请求时候才能从item中先获取image_urls列表，然后取出image_url，参数遗漏不能下载图片到本地，
    def get_media_requests(self, item, info):
        for image_url in item['image_urls']:
            print("打印出的图片url: " + image_url)
            print("正在下载" + item['title']) # 一个帖子两张图片，会打印输出两次相同的结果
            yield scrapy.Request(image_url, meta={'item': item}) # 将图片的地址传进来，请求下载

    # 确认图片是否下载完成或者没有下载
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem("Item contains no images")
        return item
            
    # 定义文件存储的路径，也是图片的存储名称，即对图片重命名
    def file_path(self, request, response=None, info=None):
        # 将item通过request传递进来
        item = request.meta['item']
        # full/是文件夹路径，full/就是放在settings中IMAGES_STORE存储文件夹shtimages下面开始，
        # 然后full文件夹里面存放下载的原始图片，缩略图会自动存放在shtimages下面的thumbs(自动创建)文件夹中
        # 图片的的名称也即定义了图片的路径

        # request.url就是上面item['image_urls']中的循环请求的url，即请求图片的地址
        # 封面图片：https://jp.netcdn.space/digital/video/mide00083/mide00083pl.jpg
        # 内容图片：https://www.assdrty.com/tupian/forum/202011/11/102921dsd631mz567gf5s0.jpg
        # 地址分割后，取最后一个值和标题进行拼接，作为图片的名称,默认图片下载在shtimages中，我们可以指定在shtimages创建一个full文件夹
        # file_name = item['title'] + request.url.split("/")[-1]
        file_name = u'full/{}-{}.jpg'.format(item['title'], request.url.split("/")[-1])
        return file_name

# '''




