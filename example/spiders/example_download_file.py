# -*- coding: utf-8 -*-
import scrapy
from ..items import DownloadItem
from scrapy.linkextractors import LinkExtractor 

"""
下载文件
"""

class ExmpleSpider(scrapy.Spider):
    name = 'downloadfiles' # spider的名字
    # 开始的爬虫地址
    start_urls = ['http://matplotlib.org/examples/index.html']
    #　默认第一个解析reponse的函数
    def parse(self, response):
        le = LinkExtractor(restrict_css='div.toctree-wrapper.compound',deny='/index.html$')
        for link in le.extract_links(response):
        	yield scrapy.Request(link.url, callback=self.parse_example)

    def parse_example(self, response):
    	href = response.css('a.reference.external::attr(href)').extract_first()
    	url = response.urljoin(href)
    	downloaditem  =DownloadItem()
    	downloaditem['file_urls'] = [url]
    	return downloaditem


"""
知识点：
    下载图片和下载文件是一样的流程，文件调用FilesPipeline，图片调用ImagesPipeline
    需要注意的是下载文件的时候item中的字段名必须为file_urls,比如这里的downloaditem['file_urls'] = [url]，
或者需要在Setting.py文件下手动制定下载链接的字段名（我忘记怎么用了，尴尬，下次想起来再回来补充吧。。。。）
"""