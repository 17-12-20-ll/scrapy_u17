# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
import pymongo
from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


class U17MysqlPipeline(object):
    def __init__(self, host, port, username, password, database):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            port=crawler.settings.get('MYSQL_PORT'),
            database=crawler.settings.get('MYSQL_DATABASE'),
            username=crawler.settings.get('MYSQL_USERNAME'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
        )

    def open_spider(self, spider):
        # 获取数据库连接
        self.db = pymysql.connect(self.host, self.username, self.password, self.database, charset='utf8',
                                  port=self.port)
        self.cursor = self.db.cursor()

    def close_spider(self):
        # 关闭数据库连接
        self.db.close()

    def process_item(self, item, spider):
        sql = 'insert into u (comic_id,name,cover,category) values (%s,%s,%s,%s)'
        self.cursor.execute(sql, (item['comic_id'], item['name'], item['cover'], item['line2']))
        self.db.commit()
        return item


class U17MongoPipeline(object):
    def __init__(self, uri, database):
        self.uri = uri
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('MONGODB_URI'),
            database=crawler.settings.get('MONGODB_DATABASE'),
        )

    def open_spider(self, spider):
        # 获取mongodb数据库连接
        self.client = pymongo.MongoClient(self.uri)
        self.db = self.client[self.database]

    def close_spider(self):
        # 关闭数据库连接
        self.client.close()

    def process_item(self, item, spider):
        self.db['manhua'].insert(dict(item))
        return item


class U17ImagePipeline(ImagesPipeline):
    # 准备图片文件名
    def file_path(self, request, response=None, info=None):
        url = request.url
        file_name = url.split('/')[-1]
        return file_name

    # 判断图片是否下载成功
    def item_completed(self, results, item, info):
        image_paths = [x['path'] for ok, x in results if ok]
        if not image_paths:
            raise DropItem('Image Downloaded Failed')
        return item

    # 指明图片下载链接,并包装成Request对象
    def get_media_requests(self, item, info):
        yield Request(item['cover'])
