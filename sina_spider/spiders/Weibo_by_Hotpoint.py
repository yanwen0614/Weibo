# -*- coding: utf-8 -*-
import json
from time import sleep

import scrapy
from scrapy.http import Request

from sina_spider.conf import SPIDERSETTING
from sina_spider.items import TopicItem


class Weibo_Hotpoint_Spider(scrapy.Spider):
    name = 'Weibo_by_Hotpoint'
    start_urls = ['https://m.weibo.cn/api/container/getIndex?containerid=100803']  # Hot topic of weibo list
    topics_api_base_url = 'https://m.weibo.cn/api/container/getIndex?'
    custom_settings = SPIDERSETTING.Weibo_Hotpoint_Spider

    def start_requests(self):
        for start_url in self.start_urls:
            yield Request(start_url, callback=self.parse_unlogin)

    def GetItem(self, hot_topic):
        item = TopicItem()
        item['Url'] = hot_topic['scheme']
        item['Category'] = hot_topic['category']
        item['Describe'] = hot_topic['desc1']
        item['Oid'] = hot_topic['actionlog']['oid']
        item['Hotlevel'] = hot_topic['desc2']
        item['Title'] = hot_topic['card_type_name']
        return item

    def parse(self, response):
        '''
        use to login first and next page or unlogin next page
        '''
        jsondata = json.loads(response.body.decode('utf-8'))
        hot_topics = jsondata['cards'][0]['card_group']
        for hot_topic in hot_topics:
            item = self.GetItem(hot_topic)
            yield item
            if self.check_emergency(item['Title']):
                redirect = self.topics_api_base_url + hot_topic['scheme'].split('?')[1]
                yield Request(redirect, callback=self.parse_topic_status)

    def parse_unlogin(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        hot_topics = jsondata['cards'][1]['card_group']+jsondata['cards'][10]['card_group']
        for hot_topic in hot_topics:
            item = self.GetItem(hot_topic)
            yield item
            if self.check_emergency(item['Title']):
                redirect = self.topics_api_base_url + hot_topic['scheme'].split('?')[1]
                yield Request(redirect, callback=self.parse_topic_status)
        yield Request(response.url+"&page=2", callback=self.parse)
        yield Request(response.url+"&page=3", callback=self.parse)

    def parse_topic_status(self):
        pass

    def check_emergency(self, title):
        # to do
        return False
