# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import re
import pymongo
from yunqiCrawl.items import YunqiBookListItem

class YunqicrawlPipeline(object):

    def __init__(self, mongo_uri, mongo_db, replicaset):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.replicaset = replicaset

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'yunqi'),
            replicaset=crawler.settings.get('REPLICASET')
        )

    # 爬虫开启时候执行该函数，仅执行一次，连接数据库
    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri, replicaset=self.replicaset)
        self.db = self.client[self.mongo_db]

    # 爬虫关闭时候执行该函数，仅执行一次，关闭数据库连接
    def close_spider(self, spider):
        self.client.close()


    def process_item(self, item, spider):
        # 判断item是否属于YunqiBookListItem，属于它，就将item数据存入数据库
        if isinstance(item, YunqiBookListItem):
            self._process_booklist_item(item)
        else:
            self._process_bookeDetail_item(item)
        return item


    # 定义两个方法用于处理小说信息和小说热度
    def _process_booklist_item(self, item):
        '''
        处理小说信息
        :param item:
        :return:
        '''
        # 向数据库yunqi中的bookInfo表中插入item数据
        self.db.bookInfo.insert(dict(item))

    def _process_bookeDetail_item(self, item):
        '''
        处理小说热度
        :param item:
        :return:
        '''
        # 需要对数据进行清洗，类似：总字数：10120，提取其中的数字
        pattern = re.compile('\d+')
        # 去掉空格和换行,标注里面有一个换行符和空格
        item['novelLabel'] = item['novelLabel'].strip().replace('\n', '')

        match = pattern.search(item['novelAllClick'])
        item['novelAllClick'] = match.group() if match else item['novelAllClick']

        match = pattern.search(item['novelMonthClick'])
        item['novelMonthClick'] = match.group() if match else item['novelMonthClick']

        match = pattern.search(item['novelWeekClick'])
        item['novelWeekClick'] = match.group() if match else item['novelWeekClick']

        match = pattern.search(item['novelAllPopular'])
        item['novelAllPopular'] = match.group() if match else item['novelAllPopular']

        match = pattern.search(item['novelMonthPopular'])
        item['novelMonthPopular'] = match.group() if match else item['novelMonthPopular']

        match = pattern.search(item['novelWeekPopular'])
        item['novelWeekPopular'] = match.group() if match else item['novelWeekPopular']

        match = pattern.search(item['novelAllComm'])
        item['novelAllComm'] = match.group() if match else item['novelAllComm']

        match = pattern.search(item['novelMonthComm'])
        item['novelMonthComm'] = match.group() if match else item['novelMonthComm']

        match = pattern.search(item['novelWeekComm'])
        item['novelWeekComm'] = match.group() if match else item['novelWeekComm']

        self.db.bookhot.insert(dict(item))

