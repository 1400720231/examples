# -*- coding: utf-8 -*-
import scrapy
from ..items import DownloadItem
from scrapy.linkextractors import LinkExtractor 



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