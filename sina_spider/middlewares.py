# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
from random import randint, random
from time import sleep

from scrapy import signals
from scrapy.downloadermiddlewares.retry import RetryMiddleware


class SinaSpiderRetryMiddleware(RetryMiddleware):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.
    def __init__(self, setting):
        self.logger = logging.getLogger(__name__)
        super().__init__(setting)

    def process_response(self, request, response, spider):
        if response.status in self.retry_http_codes:
            sleeptime = (1+request.meta.get('retry_times', 0))*random()*120
            self.logger.info('_______________Sleep__{}___sec________________'.format(sleeptime))
            self.logger.info(str(response.status)+'\t\t'+str(request.meta.get('retry_times', 0)))
            self.logger.info(str(response.url))
            sleep(sleeptime)
        return super().process_response(request, response, spider)

    def process_exception(self, request, exception, spider):
        self.logger.info(exception)
        return super().process_exception(request, exception, spider)
    

    def _retry(self, request, reason, spider):

        return super()._retry(request, reason, spider)
