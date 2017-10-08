# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class TweetsItem(Item):
    # define the fields for your item here like:
    Author = Field()
    Title = Field()
    Create_time = Field()
    Id = Field()
    Context = Field()
    Source = Field()
    Url = Field()


class TopicItem(Item):
    Url = Field()
    Title = Field()
    Category = Field()
    Describe = Field()
    Id = Field()
    Hotlevel = Field()
    Time = Field()

def main():
    item = TopicItem()
    pass

if __name__ == '__main__':
    main()