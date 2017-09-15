# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

<<<<<<< HEAD
from random import randint, random
=======
from random import randint, random, r
>>>>>>> 8608a2f799eaa4871a0c5fb3d869eea89ff23fe9
from time import sleep

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class SinaSpiderRetryMiddleware(RetryMiddleware):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
<<<<<<< HEAD
    def process_response(self, request, response, spider):
        return super().process_response(request, response, spider)

    def process_exception(self, request, exception, spider):
        return super().process_exception(request, exception, spider)
    

    def _retry(self, request, reason, spider):
        print('_______________Sleep_____________________')
        sleep(randint(1, 3)*random()*600)
        return super()._retry(request, reason, spider)
=======
    def _retry(self, request, reason, spider):
        sleep(randint(1, 3)*random()*3600)
        super()._retry(request, reason, spider)
>>>>>>> 8608a2f799eaa4871a0c5fb3d869eea89ff23fe9
