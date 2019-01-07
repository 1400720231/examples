# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
import json


"""
下载图片
"""
class ExmpleSpider(scrapy.Spider):
    name = 'downloadimages' # spider的名字
    base_url = 'http://image.so.com/zj?ch=art&sn=%s&listtype=new&temp=1'
    start_index = 0
    # 开始的爬虫地址
    start_urls = [base_url%0]
    #　默认第一个解析reponse的函数
    def parse(self, response):
        infos = json.loads(response.body.decode('utf-8'))
        # 这里没有定义item, 但是还是按照图片下载规则定义数据字段："image_url" = [] 
        print({"image_urls":[info['qhimg_url'] for info in infos['list']]})
        yield {"image_urls":[info['qhimg_url'] for info in infos['list']]}
        self.start_index += infos['count']
        if infos['count'] >0 and self.start_index<1000:
            yield Request(self.base_url%self.start_index,callback=self.parse)     
"""
下载图片和下载文件是一样的流程，
文件调用FilesPipeline
图片调用ImagesPipeline

有一个值注意的是，这个例子中的360图片站禁止爬虫，scrapy默认遵守机器人协议(ROBOT_OBEY)
所以下载不到数据，吧setting.py下的ROBOTSTXT_OBEY = True改为False即可
    # Obey robots.txt rules
    ROBOTSTXT_OBEY = False
"""