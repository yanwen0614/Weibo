import json
from time import sleep

import scrapy
from lxml import etree
from scrapy.http import Request

from ..conf import SPIDERSETTING
from ..items import TweetsItem
from ..utils.cookies import Cookies
from ..utils.user import UserSet


class Weibo_PersonPage_Spider(scrapy.Spider):
    name = "Weibo_by_PersonPage"
    start_urls = ["https://m.weibo.cn/home/me?format=cards"]
    custom_settings = SPIDERSETTING.Weibo_PersonPage_Spider
    followerlist_api_base_url = 'https://m.weibo.cn/api/container/getSecond?'
    Tweets_api_base_url = 'https://m.weibo.cn/api/container/getIndex?'

    def __init__(self):
        self.cookies = Cookies()

    def start_requests(self):
        username = '13072781826'
        for start_url in self.start_urls:
            yield Request(start_url,
                    cookies=self.cookies.getCookies(username),
                    meta={'cookiejar': 1}, callback=self.parse)

    def parse(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        scheme = jsondata[0]['card_group'][1]['apps'][1]['scheme'].split('?')[1]
        followers_url = self.followerlist_api_base_url + scheme
        yield Request(followers_url, meta={'cookiejar': 1}, callback=self.parse_get_followerlist)

    def parse_get_followerlist(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        try:
            maxpage = jsondata['maxPage']
            followers = jsondata['cards']
            for follower in followers:
                containerid = '&containerid=107603'+str(follower['user']['id'])
                url = follower['scheme'].split('?')[1] + containerid  # 得到api参数
                yield Request(self.Tweets_api_base_url+url, callback=self.parse_get_followers_Tweets)
            for i in range(1, int(maxpage)):
                yield Request(response.url.split('&')[0]+'&page={}'.format(i+1), callback=self.parse_get_followerlist)
        except:
            print(response.url)

        'To do detect whether reach the end of timeline stastues'

    def parse_get_followers_Tweets(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        statuses = jsondata['cards']
        for statuse in statuses:
            if statuse['card_type'] != 9:
                continue
            yield Request(statuse['scheme'], meta={'cookiejar': 1}, callback=self.parse_Tweets)
        yield 
    
    def parse_Tweets(self, response):
        text = response.body.decode('utf-8')
        tree = etree.HTML(text)
        jsondata = json.loads(tree.xpath('body/script/text()')[0].split('render_data = [')[1].split('][0] ||')[0])
        statuse = jsondata['status']
        item = TweetsItem()
        item['Id'] = statuse['id']
        try:
            item['Title'] = statuse['page_info']['page_title']
        except:
            item['Title'] = ''
        item['Create_time'] = statuse['created_at']
        item['Context'] = statuse['text']
        item['Author'] = statuse['user']['screen_name']
        item['Source'] = statuse['source']
        yield item
