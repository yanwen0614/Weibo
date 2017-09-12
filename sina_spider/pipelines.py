# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json


class TweetsItemPipeline(object):

    def open_spider(self, spider):
        self.file = open('TweetsItems.jl', 'w', encoding='utf-8')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(dict(item), ensure_ascii=False, sort_keys=True) + "\n"
        self.file.write(line,)
        self.file.flush()
        return item


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