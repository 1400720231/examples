# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
"""
splash动态网站爬虫，并且执行js语句
"""
# 定义一个执行下拉操作的lua脚本，来实现京东下拉加载剩余部分数据的操作
lua_script = """
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('pn-next)[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end
"""



class JdBookSpider(scrapy.Spider):
    name = 'jd_book'
    allowed_domains = ['search.jd.com']
    # start_urls = ['http://search.jd.com/']
    base_url = "https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&book=y&vt=2&wq=python&page={PAGE}"

    def start_requests(self):
        # yield scrapy.Request(self.base_url.format(1), callback=self.parse_urls, dont_filter=True)
        yield SplashRequest(self.base_url.format(PAGE=1), endpoint="execute",
                                args={"lua_source":lua_script},
                                cache_args=["lua_source"],meta={"page":1},callback=self.parse_urls)
    def parse_urls(self, response):
        
        # 获取每一页的书本的名字和价格
        for sel in response.css("ul.gl-warp.clearfix > li.gl-item"):
            name = sel.css("div.p-name").xpath("string(.//em)").extract_first()
            price = sel.css("div.p-price i::text").extract_first()
            yield {"name":name,"price":price}

        next_page = response.css(".pn-next")
        if next_page:
            pageNum =  response.meta["page"] +2
            # next_url = response.urljoin(next_page.css("attr(href)").extract_first())
            next_url = self.base_url.format(PAGE=pageNum)
            yield SplashRequest(next_url, endpoint="execute",args={"lua_source":lua_script},cache_args=["lua_source"],meta={"page":pageNum},callback=self.parse_urls)

"""
（１）
首先来讲解lua_script脚本的含义：
function main(splash)
    splash:go(splash.args.url)
    splash:wait(2)
    splash:runjs("document.getElementsByClassName('pn-next)[0].scrollIntoView(true)")
    splash:wait(2)
    return splash:html()
end

访问splash.args.url，也就是SplashRequest(url）中的url,等待２秒，执行js脚本，js脚本的含义是，向下滚懂直到找到
属性名字为pn-next的位置为止，等待２秒，返回加载完成渲染的html.

（２）
SplashRequest所有参数：
class SplashRequest(scrapy.Request):
    def __init__(self,
                     url=None,
                     callback=None,
                     method='GET',
                     endpoint='render.html',
                     args=None,
                     splash_url=None,
                     slot_policy=SlotPolicy.PER_DOMAIN,
                     splash_headers=None,
                     dont_process_response=False,
                     dont_send_headers=False,
                     magic_response=True,
                     session_id='default',
                     http_status_from_error_code=True,
                     cache_args=None,
                     meta=None,
                     **kwargs):
                     中间省略
    super(SplashRequest, self).__init__(url, callback, method, meta=meta,
                                                **kwargs)
可以看到SplashRequest继承于scrapy.Request，也就是说SplashRequest拥有scrapy.Request参数功能，
并且还增加了endpoint这些特定的splash的参数


（３）

<1>SplashRequest(url, args={"images":0, "timeout":3})

<2>SplashRequest(next_url, endpoint="execute",
            args={"lua_source":lua_script},
            cache_args=["lua_source"],
            meta={"page":pageNum},callback=self.parse_urls)
    如果这是加载js页面就使用<1>,直接加载返回。如果使用执行js语句就使用类似<2>.
其中需要强调的是endpoint="execute"表示执行js的端点，不然执行不了js。
args={"lua_source":lua_script}声明了脚本，参数必读为“lua_source”。
cache_args=["lua_source"]参数可有可无，这个参数的意思是吧脚本“lua_source”加载
到splash服务器，下次直接调用。
"""
