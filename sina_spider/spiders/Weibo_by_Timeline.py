import json
from time import sleep

import scrapy
from scrapy.http import Request

from sina_spider.conf import SPIDERSETTING
from sina_spider.items import TweetsItem
from sina_spider.utils.cookies import Cookies
from sina_spider.utils.user import UserSet


class Weibo_Timeline_Spider(scrapy.Spider):
    name = "Weibo_by_Timeline"
    start_urls = ["https://m.weibo.cn/feed/friends?"]
    custom_settings = SPIDERSETTING.Weibo_Timeline_Spider

    def __init__(self):
        super().__init__()
        self.cookies = Cookies()

    def start_requests(self):
        username = str(SPIDERSETTING.Weibo_Timeline_Spider_login_user)
        for start_url in self.start_urls:
            yield Request(start_url,
                    cookies=self.cookies.getCookies(username),
                    meta={'cookiejar': 1}, callback=self.parse_get_page)

    def parse_get_page(self, response):
        try:
            base_num = int(response.url.split('=')[-1])
        except:
            base_num = 1
        next_url = response.url.split('?')[0]+'?page={}'
        jsondata = json.loads(response.body.decode('utf-8'))
        if jsondata['statuses'] == False:
            return
        for statuse in jsondata['statuses']:
            yield self.parse_get_item_inf(statuse)
        '''for page_num in range(1, 10):
        # yield scrapy.Request(next_url.format(base_num + 1), meta={'cookiejar': 1}, callback=self.parse_get_item_inf) '''
        yield scrapy.Request(next_url.format(base_num + 1), meta={'cookiejar': 1}, callback=self.parse_get_page)  # next page

    def parse_get_item_inf(self, statuse):
        item = TweetsItem()
        item['Id'] = statuse['id']
        try:
            item['Title'] = statuse['page_info']['page_title']
        except KeyError:
            item['Title'] = ''
        item['Create_time'] = statuse['created_at']
        item['Context'] = statuse['text']
        item['Author'] = statuse['user']['screen_name']
        item['Source'] = statuse['source']
        return item

