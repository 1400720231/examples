# -*- coding: utf-8 -*-
import scrapy


class LoginCookie(scrapy.Spider):
    name = 'cookie'
    start_urls = ['https://www.zhihu.com/people/tian-geng-shang-de-python/activities']

    def parse(self, response):
        if "田埂" in response.text:
            print("登录成功，已经能看到个人信息！！！")
        else:
            print("登录失败")

"""
知识点：
    １：记得在setting中配置：
        DOWNLOADER_MIDDLEWARES = {
           #　因为默认系统的CookiesMiddleware是开始的，所以我们重用并且赋值为None,让他失效
           'scrapy.downloadermiddlewares.cookies.CookiesMiddleware':None,
           'example.middlewares.CustomerCookiesMiddleware':701,
        }
    ２：记得在setting中配置user-agent,因为知乎对此做了反爬虫限制
        
        USER_AGENT = 'Mozilla/5.0 (X11; Ubuntu) Gecko/20100101 Firefox/62.0'
        ROBOTSTXT_OBEY = False
"""