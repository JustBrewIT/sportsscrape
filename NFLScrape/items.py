# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NFLScrapeItem(scrapy.Item):
    SiteTypeID = scrapy.Field()
    FirstName = scrapy.Field()
    LastName = scrapy.Field()
    TeamName = scrapy.Field()
    PositionName = scrapy.Field()
    Height = scrapy.Field()
    Weight = scrapy.Field()
    Age = scrapy.Field()
    Date = scrapy.Field()


