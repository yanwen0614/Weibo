from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from sina_spider.spiders.Weibo_by_Hotpoint import Weibo_Hotpoint_Spider
from sina_spider.spiders.Weibo_by_PersonPage import Weibo_PersonPage_Spider
from sina_spider.spiders.Weibo_by_Timeline import Weibo_Timeline_Spider

process = CrawlerProcess(get_project_settings())
#process.crawl(Weibo_Timeline_Spider)
process.crawl(Weibo_Hotpoint_Spider)
process.crawl(Weibo_PersonPage_Spider)
process.start()
