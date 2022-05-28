# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql

'''
pipeline文件，处理数据库连接和插入
'''


class XcPipeline:

    # 由于pipeline需要构建数据库的连接参数，所以要使用类方法来手动生成对象
    def __init__(self, host, port, db, usr, password):
        self.host = host
        self.port = port
        self.db = db
        self.usr = usr
        self.password = password

    @classmethod
    def from_crawler(cls, clawer):
        host = clawer.settings.get("SQL_HOST")
        password = clawer.settings.get("SQL_PASSWORD")
        db = clawer.settings.get("SQL_DB")
        port = clawer.settings.get("SQL_PORT")
        usr = clawer.settings.get("SQL_USR")
        return cls(host, port, db, usr, password)

    def process_item(self, item, spider):
        # 进行数据清洗和插入
        try:
            item['usr_ID'] = int(item['usr_ID'])
            self.cursor.execute('INSERT into xc VALUES({},"{}","{}","{}")'.format(
                item['usr_ID'], item['contents'], item['usr_name'], item['img_url_list']))
        except:
            pass
        # return item

    def open_spider(self, spider):
        # 启动时开启数据库
        self.connection = pymysql.connect(
            host=self.host,
            port=self.port,
            user=self.usr,
            password=self.password,
            database=self.db,
            autocommit=True)
        self.cursor = self.connection.cursor()

    def close_spider(self, spider):
        # 结束时关闭数据库
        self.cursor.close()
        self.connection.close()
