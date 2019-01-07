# -*- coding: utf-8 -*-
import scrapy
from ..items import ExampleItem

"""
保存数据库
"""
class ExmpleSpider(scrapy.Spider):
    name = 'booksmysqlpipeline' # spider的名字
    # 开始的爬虫地址
    start_urls = ['http://books.toscrape.com/']
    #　默认第一个解析reponse的函数
    def parse(self, response):
        
        for book in response.css('article.product_pod'):
            name = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()
            #　用item形式返回提取的数据
            bookitem = ExampleItem()
            bookitem['name'] = name
            bookitem['price'] = price
            # 这里一定要用yield,不然代码只执行一次解析就结束了
           
            yield bookitem
        # 爬虫下一页
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:

            # 获取此时的url相对项目的绝对url
            next_url = response.urljoin(next_url)
            # 参考源码实现的第一个response一样，访问下一页并且把下一页的reponse回调给self.parse函数，直到没有下一页停止
            yield scrapy.Request(next_url, callback=self.parse)
        

"""
知识点：
    主要内容在pipelines中，需要编写保存到数据库中的pipeline,然后记得在setting.py中配置：
ITEM_PIPELINES = {
    ...
   'example.pipelines.MYSQLPipeline': 301,
    ...
}

"""