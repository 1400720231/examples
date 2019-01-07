# -*- coding: utf-8 -*-
import scrapy

from scrapy_splash import SplashRequest


"""
splash动态网站爬取，没有执行js语句
"""
class QuoteSpider(scrapy.Spider):
    name = 'quote'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/js/']

    # 重载start_requests方法
    def start_requests(self):
    	for url in self.start_urls:
    		yield SplashRequest(url, args={"images":0,"timeout":3})

    def parse(self, response):
        for sel in response.css("div.quote"):
        	quote = sel.css("span.text::text").extract_first()
        	author = sel.css("small.author::text").extract_first()
        	yield {"quote":quote, "author":author}

        href = response.css("li.next > a::attr(href)").extract_first()
        if href:
        	url = response.urljoin(href)
        	yield SplashRequest(url, args={"images":0, "timeout":3})


"""
知识点：

（1） 在settings.py下配置相关内容：

# splash render.html端点地址
SPLASH_URL = "http://localhost:8050"

# splash 去重过滤器，具体是过滤什么的我也不晓得。。。
DUPEFILTER_CLASS = "scrapy_splash.SplashAwareDupeFilter"

# 用来支持SplashRequest中的cache_args参数的配置
SPIDER_MIDDLEWARES = {
   # 'example.middlewares.ExampleSpiderMiddleware': 543,
   'scrapy_splash.SplashDeduplicateArgsMiddleware':100,
}


DOWNLOADER_MIDDLEWARES = {
   #
   ...
   # 下面三个是对应splash的相关配置

   "scrapy_splash.SplashCookiesMiddleware":723, # 开启相关scrapy_splash中间件
   "scrapy_splash.SplashMiddleware":725, # 开启相关scrapy_splash中间件
   # 调整系统scrapy内部中间件的顺序
   "scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware":810,
   ...
}

（2）docker开启splash服务
刚开始我以为pip install scrapt_splash之后就默认开启了splash服务，是我太天真。。。
docker run -p 8050:8050 scraping/splash
这里的8050可以随便取的，但是一定要和setting.py中配置的SPLASH_URL的端口一致：
	SPLASH_URL = "http://localhost:8050"



"""