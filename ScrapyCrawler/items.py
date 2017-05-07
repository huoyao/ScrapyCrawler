# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class TuicoolItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    imageUrl = scrapy.Field()
    articleTitle = scrapy.Field()
    articleUrl = scrapy.Field()
    articleContent = scrapy.Field()
    articleSourceName = scrapy.Field()
    articleSourceUrl = scrapy.Field()
    publishDateTime = scrapy.Field()
    pass
