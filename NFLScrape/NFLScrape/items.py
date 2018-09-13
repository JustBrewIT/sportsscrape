# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class RetailScrapeItem(scrapy.Item):
    AddressLine = scrapy.Field()
    StoreName = scrapy.Field()
    StoreNumber = scrapy.Field()
    StoreType = scrapy.Field()
    Street = scrapy.Field()
    City = scrapy.Field()
    State = scrapy.Field()
    Zip = scrapy.Field()
    Country = scrapy.Field()
    Suite = scrapy.Field()
    PhoneNumber = scrapy.Field()
    FaxNumber = scrapy.Field()
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
