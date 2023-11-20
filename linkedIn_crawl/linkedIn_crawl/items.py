# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LinkedinCrawlItem(scrapy.Item):
    # define the fields for your item here like:
     name = scrapy.Field()
     profile_url = scrapy.Field()
     title = scrapy.Field()
     gettest = scrapy.Field()
     links = scrapy.Field()



