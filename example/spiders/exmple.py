# -*- coding: utf-8 -*-
import scrapy

class ExmpleSpider(scrapy.Spider):
    name = 'books' # spider的名字
    # 开始的爬虫地址
    start_urls = ['http://books.toscrape.com/']
    #　默认第一个解析reponse的函数
    def parse(self, response):
        for book in response.css('article.product_pod'):
        	name = book.xpath('./h3/a/@title').extract_first()
        	price = book.css('p.price_color::text').extract_first()
            #　返回提取的数据
        	yield {
        		'name':name,
        		'price':price
        	}
        # 爬虫下一页
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 获取此时的url相对项目的绝对url
        	next_url = response.urljoin(next_url)
            # 参考源码实现的第一个response一样，访问下一页并且把下一页的reponse回调给self.parse函数，直到没有下一页停止
        	yield scrapy.Request(next_url, callback=self.parse)


"""
第一个scarpy联系的的例子
主要是了解熟悉scrapy的流程以及他的工作流走向
知识点：
    必须重载parse解析函数
    callback　指定下一个解析reponse的函数，这里用的是callback=self.parser
    response.urljoin(url): 自动拼接成在start_urls=[]基础上的绝对路径，这样就不会有错
    xpath css 语法，很重要的有好多地方都用用到，基本贯穿整个爬虫体系
"""