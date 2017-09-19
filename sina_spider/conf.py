import os

root = os.getcwd()



class DATABASE(object):
        user = 'root'
        pw = 'casm'
        host = 'localhost'
        post = '3306' # default
        charset = 'UTF8' 
        dbname = 'weibo_temp'


class SPIDERSETTING(object):
    Weibo_Timeline_Spider = {
        'ITEM_PIPELINES' : {'sina_spider.pipelines.TweetsTimelineItemPipeline': 300}
    }

    Weibo_Hotpoint_Spider = {
        'ITEM_PIPELINES' : {'sina_spider.pipelines.HotTopicItemPipeline': 300}
    }

    Weibo_PersonPage_Spider = {
        'ITEM_PIPELINES' : {
                                'sina_spider.pipelines.TweetsPersonPageItemPipeline': 300,
                               # 'sina_spider.pipelines.TweetsPersonPageItem_DataBase_Pipeline': 300
                                
                            },
        'LOG_LEVEL' : 'INFO',
        'JOBDIR' : 'Weibo_PersonPage_Spider'
    }

    Weibo_Timeline_Spider_login_user = 18515393545
    Weibo_PersonPage_Spider_login_user = 18515393545
