# -*- coding: utf-8 -*-


import configparser
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from os import sep as ossep

import pymysql

try:
    import sina_spider.utils.Database as Utils_DB
    from sina_spider.conf import DATABASE, cfgfilename
    from sina_spider.items import TopicItem, TweetsItem
except ImportError:
    import utils.Database as Utils_DB
    from conf import DATABASE, cfgfilename
    from items import TopicItem, TweetsItem


class MyBaisePipeline(object):
    _last_item_id = None  # monitor process reach last position
    cfgfile = None
    file = None

    def __init__(self):
        self.cfgfile = configparser.ConfigParser()  # read get last id
        self.cfgfile.read(cfgfilename)
        try:
            self._last_item_id = self.cfgfile.get('last_item_id', __name__)
        except:
            pass
            
    def open_spider(self, spider):    
        self.file = open(ossep.join(('.', 'result', 'ProblemUrl'+__name__+'.jl')), 'a+', encoding='utf-8')
        
    def process_item(self, item, spider):
        self._last_item_id = item['Id']

    def close_spider(self, spider):
        self.cfgfile.set('last_item_id', __name__, self._last_item_id)
        with open(cfgfilename, 'w') as configfile:
            self.cfgfile.write(configfile)


class MyBaise_DataBase_Pipeline(object):
    _db = None
    insert = ''

    def Create_createtable_sql(self, tablename, Key, **kwarg):
        return Utils_DB.Create_createtable_sql(tablename, Key, **kwarg)

    def Create_insert_sql(self, tablename, *arg):
        return Utils_DB.Create_insert_sql(tablename, *arg)
        
    def open_spider(self, spider):
        self.stats = spider.crawler.stats
        
        self._db = pymysql.connect(host='localhost',
                                    user=DATABASE.user,
                                    password=DATABASE.pw,
                                    db=DATABASE.dbname,
                                    charset=DATABASE.charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self._db.cursor()
    
    def process_item(self, item, spider):
        try:
            vls = [vl for vl in map(lambda x: item[x], sorted(item.fields.keys()))]
            self.cur.execute(self.insert.format(*vls))
            self._db.commit()
        except:
            self.stats.inc_value('cannot_parse/count')
            self.file.writeline(item["Url"]+'\n')
            self.file.flush()

    def create_table():
        pass


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
        MyBaisePipeline.process_item(self, item, spider)
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
        MyBaisePipeline.process_item(self, item, spider)
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class TweetsPersonPageItem_DataBase_Pipeline(MyBaisePipeline, MyBaise_DataBase_Pipeline):
    
    insert = ''

    def __init__(self):
        super().__init__()
        self.insert = self.Create_insert_sql('tweets',  *sorted(TweetsItem().fields.keys()))

    def open_spider(self, spider):
        MyBaisePipeline.open_spider(self, spider)
        MyBaise_DataBase_Pipeline.open_spider(self, spider)
       
    def close_spider(self, spider):
        self._db.close()
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        MyBaisePipeline.process_item(self, item, spider)
        MyBaise_DataBase_Pipeline.process_item(self, item, spider)
    



class HotTopicItemPipeline(MyBaisePipeline):

    def __init__(self):
        super().__init__()

    def open_spider(self, spider):
        self.file = open('HotTopicItems.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        MyBaisePipeline.process_item(self, item, spider)
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class HotTopicItem_DataBase_Pipeline(MyBaisePipeline, MyBaise_DataBase_Pipeline):
    insert = ''

    def __init__(self):
        super().__init__()
        self.insert = self.Create_insert_sql('Hot_topic', *sorted(TopicItem().fields.keys()))

    def open_spider(self, spider):
        MyBaisePipeline.open_spider(self, spider)
        MyBaise_DataBase_Pipeline.open_spider(self, spider)
        
    def close_spider(self, spider):
        self._db.close()
        self.file.close()
        super().close_spider(spider)

    def process_item(self, item, spider):
        MyBaisePipeline.process_item(self, item, spider)
        MyBaise_DataBase_Pipeline.process_item(self, item, spider)



def main():
    db = pymysql.connect(host=DATABASE.host,
                                    user=DATABASE.user,
                                    password=DATABASE.pw,
                                    db=DATABASE.dbname,
                                    charset=DATABASE.charset,
                                    cursorclass=pymysql.cursors.DictCursor)
    print(db)
if __name__ == '__main__':
    main()