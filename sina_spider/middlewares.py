# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from random import randint, random, r
from time import sleep

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class SinaSpiderRetryMiddleware(RetryMiddleware):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def _retry(self, request, reason, spider):
        sleep(randint(1, 3)*random()*3600)
        super()._retry(request, reason, spider)
