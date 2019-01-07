# -*- coding: utf-8 -*-
import scrapy

"""
表单登录
"""
class ZhiHuSpider(scrapy.Spider):
    name = 'zhihu'
    login_url = 'http://example.webscraping.com/places/default/user/login?_next=/places/default/index'

    # 重载start_requests方法，控制出事请求url
    def start_requests(self):
        yield scrapy.Request(url=self.login_url, callback=self.login)

    # 把利用FormRequest.from_response方法传入账号密码登录，也可以采用FormRequest传入所有参数
    def login(self, response):
        formdata = {'email':'youremail', 'password':'yourpassword'}
        yield scrapy.FormRequest.from_response(response, formdata=formdata, callback=self.detail)

    # 详细处理逻辑函数，这里省略.
    def detail(self, response):
        if 'panda' in response.text:
            print('6666666666666666666666')