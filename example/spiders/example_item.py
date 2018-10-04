# -*- coding: utf-8 -*-
import scrapy
from ..items import ExampleItem
num =0

class ExmpleSpider(scrapy.Spider):
    name = 'booksitem' # spider的名字
    # 开始的爬虫地址
    start_urls = ['http://books.toscrape.com/']
    #　默认第一个解析reponse的函数
    num =0
    def parse(self, response):
        
        for book in response.css('article.product_pod'):
            name = book.xpath('./h3/a/@title').extract_first()
            price = book.css('p.price_color::text').extract_first()
            #　用item形式返回提取的数据
            bookitem = ExampleItem()
            bookitem['name'] = name
            bookitem['price'] = price
            # 这里一定要用yield　如果用return 整个函数在这里就结束了
            #而且输出的内容一条也没有，因为整个parse解析函数是按照生成器的体系来的，
            # 当你执行next内容的时候返回一个的值，所以当执行到第二个数据解析的时候再reurn
            # 的话应该会后第一条数据的记录,比如我第二次才return 那么第一次解析的内容应该是存在的
            # 也就是会保存第一页的数据20个(已经测试过的确是这样的)
            if self.num ==1:
                return bookitem
            else:

                yield bookitem
        # 爬虫下一页
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:

            # 获取此时的url相对项目的绝对url
            next_url = response.urljoin(next_url)
            # 参考源码实现的第一个response一样，访问下一页并且把下一页的reponse回调给self.parse函数，直到没有下一页停止
            yield scrapy.Request(next_url, callback=self.parse)
        self.num +=1

"""
第一个scarpy联系的的例子
主要是了解熟悉scrapy的流程以及他的工作流走向
知识点：
    必须重载parse解析函数
    callback　指定下一个解析reponse的函数，这里用的是callback=self.parser
    response.urljoin(url): 自动拼接成在start_urls=[]基础上的绝对路径，这样就不会有错
    xpath css 语法，很重要的有好多地方都用用到，基本贯穿整个爬虫体系

    ------新增笔记-----
    ExampleItem实例化后一定要yield回去，不能能用return ，整个parse函数解析的时候是按照迭代器的
    形式来执行的，如果return 整个函数都结束了，整个爬虫代码在第一页完成后会停止，而且没有数据，因为根据迭代器规则，
    当你执行next的时候才返回上一个数据。也就是说到第二页的时候你才打得到第一页的数据。

    值得注意的是我只是实例化了ExampleItem,但是没有在写一个item pipline，也一样能执行成功，相当于这个ExampleItem
    无效，如同前面的直接yield {'name':name,'price':price}一样
"""