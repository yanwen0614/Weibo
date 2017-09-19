# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
import pymysql
from sina_spider.conf import DATABASE


class TweetsTimelineItemPipeline(object):
    file = None

    def open_spider(self, spider):
        self.file = open('TweetsItemsTimeline.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class TweetsPersonPageItemPipeline(object):
    file = None

    def open_spider(self, spider):
        self.file = open('TweetsItemsPersonPage.jl', 'a+', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


class TweetsPersonPageItem_DataBase_Pipeline(object):

    file = None
    _db = None
    insert = '''INSERT INTO Tweets ( id, time, text )  VALUES  ( '{}', '{}','{}'); '''
    def open_spider(self, spider):
        self.stats = spider.crawler.stats
        self.file = open('ProblemUrl.jl', 'a+', encoding='utf-8')
        self._db =  pymysql.connect(host='localhost',
                                    user=DATABASE.user,
                                    password=DATABASE.pw,
                                    db=DATABASE.dbname,
                                    charset=DATABASE.charset,
                                    cursorclass=pymysql.cursors.DictCursor)
        self.cur = self._db.cursor()
        
    def close_spider(self, spider):
        self._db.close()
        self.file.close()

    def process_item(self, item, spider):
        try:
            self.cur.execute(self.insert.format(item['Id'],item['Create_time'],item['Context'].replace("'","|")))
            self._db.commit()
        except :
            self.stats.inc_value('cannot_parse/count')
            self.file.writeline(item["Url"])
            self.file.flush()




class HotTopicItemPipeline(object):

    def open_spider(self, spider):
        self.file = open('HotTopicItems.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item