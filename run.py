from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from sina_spider.spiders.Weibo_by_Timeline import Weibo_Timeline_Spider
from sina_spider.spiders.Weibo_by_Hotpoint import Weibo_Hotpoint_Spider
from sina_spider.spiders.Weibo_by_PersonPage import Weibo_PersonPage_Spider

process = CrawlerProcess(get_project_settings())
#process.crawl(Weibo_Timeline_Spider)
#process.crawl(Weibo_Hotpoint_Spider)
process.crawl(Weibo_PersonPage_Spider)
process.start()




'''def text(next_url="https://m.weibo.cn/feed/friends?"):
    try:
        base_num = int(next_url.split('=')[1])
    except:
        base_num = 0
    next_url = next_url.split('?')[0]+'?page={}'
    for page_num in range(10):
        print(next_url.format(base_num + page_num + 1))
    print(next_url.format(base_num + 10)+'\t\t SSS')

    return 0 if base_num > 90 else text(next_url.format(base_num + 10))

text()'''