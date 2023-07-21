# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CsdnspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    point=scrapy.Field()
    question=scrapy.Field()
    answer=scrapy.Field()

