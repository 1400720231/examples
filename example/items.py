# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class ExampleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = Field()
    price = Field()


class DownloadItem(scrapy.Item):
	# 用来保存所将要下载的文件的url
	file_urls =scrapy.Field()
	# 用来保存讲file_urls中的文件下载完成后返回的状态信息数据
	files = scrapy.Field()