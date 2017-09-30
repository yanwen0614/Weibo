# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from sina_spider.conf import DATABASE,cfgfilename
from os import sep as ossep
import configparser

class MyBaisePipeline(object):
    _last_item_id = None  # monitor process reach last position
    cfgfile = None
    file = None
    def __init__(self):
        self.cfgfile = configparser.ConfigParser()# read get last id
        self.cfgfile.read(cfgfilename)
        try:
            self._last_item_id = self.cfgfile.get('last_item_id',__name__)
        except KeyError:
            pass
        

    def open_spider(self, spider):    
        self.file = open(ossep.join(('result','ProblemUrl'+__name__+'.jl')), 'a+', encoding='utf-8')
        

    def close_spider(self, spider):
        self.cfgfile.get('last_item_id',__name__) = self._last_item_id
        with open(cfgfilename, 'w') as configfile:
            self.cfgfile.write(configfile)


class MyBaise_DataBase_Pipeline(object):
    _db = None

    def Create_insert_sql(tablename, *arg):
        sql = '''INSERT INTO {tablename} {}  VALUES  ({})'''.format(tablename = tablename)
        placeholder  = ["'{}'"for _ in range()]




    def open_spider(self, spider):
        self.stats = spider.crawler.stats
        
        self._db =  pymysql.connect(host='localhost',
                                    user=DATABASE.user,
                                    password=DATABASE.pw,
                                    db=DATABASE.dbname,
                                    charset=DATABASE.charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self._db.cursor()

class TweetsTimelineItemPipeline(MyBaisePipeline):
    file = None

    def __init__(self):
        super().__init__()

    def open_spider(self, spider):
        self.file = open('TweetsItemsTimeline.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class TweetsPersonPageItemPipeline(MyBaisePipeline):
    file = None

    def __init__(self):
        super().__init__()

    def open_spider(self, spider):
        self.file = open('TweetsItemsPersonPage.jl', 'a+', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class TweetsPersonPageItem_DataBase_Pipeline(MyBaisePipeline, MyBaise_DataBase_Pipeline):
    
    insert = '''INSERT INTO Tweets ( id, time, text )  VALUES  ( '{}', '{}','{}'); '''

    def __init__(self):
        super(MyBaisePipeline).__init__()

    def open_spider(self, spider):
        super(MyBaise_DataBase_Pipeline).open_spider(spider)
       
        
    def close_spider(self, spider):
        self._db.close()
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        try:
            self.cur.execute(self.insert.format(item['Id'],item['Create_time'],item['Context'].replace("'","|")))
            self._db.commit()
        except :
            self.stats.inc_value('cannot_parse/count')
            self.file.writeline(item["Url"]+'\n')
            self.file.flush()




class HotTopicItemPipeline(MyBaisePipeline):

    def __init__(self):
        super().__init__()

    def open_spider(self, spider):
        self.file = open('HotTopicItems.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item

class HotTopicItem_DataBase_Pipeline(MyBaisePipeline, MyBaise_DataBase_Pipeline):
    insert = '''INSERT INTO Tweets ( id, time, text )  VALUES  ( '{}', '{}','{}'); '''

    def __init__(self):
        super(MyBaisePipeline).__init__()

    def open_spider(self, spider):
        super(MyBaise_DataBase_Pipeline).open_spider(spider)
       
        
    def close_spider(self, spider):
        self._db.close()
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        try:
            self.cur.execute(self.insert.format(item['Id'],item['Create_time'],item['Context'].replace("'","|")))
            self._db.commit()
        except :
            self.stats.inc_value('cannot_parse/count')
            self.file.writeline(item["Url"]+'\n')
            self.file.flush()