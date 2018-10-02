# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

from scrapy.exceptions import DropItem 
class ExamplePipeline(object):
    def process_item(self, item, spider):
        name = item['name']+'--panda'
        item['name'] = name 
        if name:
            raise DropItem("哈哈，这是一条信息，当name不为空的时候我就报错DropItem这一条item就会被抛弃")
        return item

"""

DropItem错误会让scrapy直接抛弃此时进来的item，然后接着执行下一条。
我这里判断当name不为空的时候就抛弃，按道理结果应该没有输出内容
(经过实验，的确是没有数据的，并且前台会显示一条这样的数据：
2018-10-02 02:39:54 [scrapy.core.scraper] WARNING: Dropped: 哈哈，这是一条信息，当name不为空的时候我就报错DropItem这一条item就会被抛弃


)
"""
import MySQLdb
class MYSQLPipeline(object):
    host = 'localhost'
    user = 'root'
    passwd = 'root'
    db = 'scrapy'
    # 打开数据库链接
    def open_spider(self,sider):
        self.db = MySQLdb.connect(host=self.host,user=self.user,passwd=self.passwd,db=self.db, charset='utf8' )
    # 挂壁数据库链接
    def close_spider(self,spider):
        self.db.close()
    # 处理item逻辑函数
    def process_item(self, item, spider):
        name = item['name']
        price =item['price']
        # 把数据保存数据库中
        sql = "insert into scrapy(name,price) values(%s,%s)"  
        cursor =self.db.cursor()
        cursor.execute(sql,(name,price))
        self.db.commit()
        return item

"""
知识点：
    open_spider close_spider属于父类方法，这里采用重载方式完成在处理item的时候
    用open_spider打开数据库链接，然后用process_item处理数据（保存在数据库），
    然后用close_spider关闭数据库。

    而且open_spider和close_spider的顺序没有前后关系，只要定义就行了，scrapy会自己搞定的

    当然还是要在setting.py下面记得配置MYSQLPipeline !!!!!

"""




from scrapy.pipelines.files import FilesPipeline
from urllib.parse import urlparse
from os.path import basename, dirname,join
class MyFilesPipeline(FilesPipeline):
    def file_path(self, request, response=None, info=None):
        path = urlparse(request.url).path
        return join(basename(dirname(path)),basename(path))
"""
FilesPipeline是内置的文件pipeline
MyFilesPipeline继承FilesPipeline的目的是为了改写文件名生成函数，
因为默认文件名生成是根据路径最后两个子级路由生成散列值明明的。比如一个matplotlib.py文件
下载后的名字可能是这样:dasdasdasdasnjdashdoasihdoi.py。重载file_path方法就是为了让文件
下载后就是他原来文件的名字

"""