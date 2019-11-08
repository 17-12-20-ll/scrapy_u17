# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class U17Item(scrapy.Item):
    # define the fields for your item here like:
    # 漫画唯一id
    comic_id = scrapy.Field()
    # 漫画标题
    name = scrapy.Field()
    # 漫画封面
    cover = scrapy.Field()
    # 漫画标签
    line2 = scrapy.Field()
