import json
from time import sleep
import scrapy
from scrapy.http import Request

from ..items import TweetsItem
from ..utils.cookies import Cookies
from ..utils.user import UserSet
from ..conf import SPIDERSETTING


class Weibo_Timeline_Spider(scrapy.Spider):
    name = "Weibo_by_Timeline"
    start_urls = ["https://m.weibo.cn/feed/friends?"]
    custom_settings = SPIDERSETTING.Weibo_Timeline_Spider

    def __init__(self):
        self.cookies = Cookies()

    def start_requests(self):
        username = '13072781826'
        for start_url in self.start_urls:
            yield Request(start_url,
                    cookies=self.cookies.getCookies(username),
                    meta={'cookiejar': 1}, callback=self.parse_get_mutiUrls)

    def parse_get_mutiUrls(self, response):
        try:
            base_num = int(response.url.split('=')[1])
        except:
            base_num = 0
        next_url = response.url.split('?')[0]+'?page={}'
        for page_num in range(10):
            yield scrapy.Request(next_url.format(base_num + page_num + 1), meta={'cookiejar': 1}, callback=self.parse_get_item_inf)
        yield scrapy.Request(next_url.format(base_num + 10), meta={'cookiejar': 1}, callback=self.parse_get_mutiUrls)

    def parse_get_item_inf(self, response):
        jsondata = json.loads(response.body.decode('utf-8'))
        statuses = jsondata['statuses']

        'To do detect whether reach the end of timeline stastues'

        for statuse in statuses:
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
        del jsondata

