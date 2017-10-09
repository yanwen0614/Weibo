from os import getcwd, makedirs
from sys import path

from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from sina_spider.spiders.Weibo_by_Hotpoint import Weibo_Hotpoint_Spider
from sina_spider.spiders.Weibo_by_PersonPage import Weibo_PersonPage_Spider
from sina_spider.spiders.Weibo_by_Timeline import Weibo_Timeline_Spider

path.append(getcwd())

try:
    makedirs('log')
    makedirs('result')
except FileExistsError:
    pass

process = CrawlerProcess(get_project_settings())
#process.crawl(Weibo_Timeline_Spider)
process.crawl(Weibo_Hotpoint_Spider)
process.crawl(Weibo_PersonPage_Spider)
process.start()
<<<<<<< HEAD



=======
>>>>>>> b2a6858a0ae4261f2be1234213894abb2888ad58
