import os

root = os.getcwd()

class DATABASE(object):
        user = ''
        pw = ''
        host = ''
        post = ''


class SPIDERSETTING(object):
    Weibo_Timeline_Spider = {
        'ITEM_PIPELINES' : {'sina_spider.pipelines.TweetsTimelineItemPipeline': 300}
    }

    Weibo_Hotpoint_Spider = {
        'ITEM_PIPELINES' : {'sina_spider.pipelines.HotTopicItemPipeline': 300}
    }

    Weibo_PersonPage_Spider = {
        'ITEM_PIPELINES' : {'sina_spider.pipelines.TweetsPersonPageItemPipeline': 300}
    }

    Weibo_Timeline_Spider_login_user = 18515393545
    Weibo_PersonPage_Spider_login_user = 18515393545
