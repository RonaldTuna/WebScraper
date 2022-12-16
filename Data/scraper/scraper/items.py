# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    Name = scrapy.Field()
    ID = scrapy.Field()
    Commercial_Registered_Agent = scrapy.Field()
    Registered_Agent = scrapy.Field()
    Owner = scrapy.Field()
