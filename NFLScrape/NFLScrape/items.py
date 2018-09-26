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
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    DMFullName = scrapy.Field()
    DMFirstName = scrapy.Field()
    DMLastName = scrapy.Field()
    DMPhoneNumber = scrapy.Field()
    DMEMailAddress = scrapy.Field()
    DMTitle = scrapy.Field()
    MailingAddr= scrapy.Field()
    MailingAddrCity = scrapy.Field()
    MailingAddrState = scrapy.Field()
    MailingAddrZip = scrapy.Field()
    ComingSoon = scrapy.Field()
    ClosingSoon = scrapy.Field()
    ScraperTargetID = scrapy.Field()
    AgentID = scrapy.Field()
