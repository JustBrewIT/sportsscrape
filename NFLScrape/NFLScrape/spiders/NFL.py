import scrapy
import NFLScrape
from NFLScrape import NFLScrapeItem
import logging
import re
import json
import unidecode


class NFL(NFLScrape.NFLSpider):
    name = 'NFL'
    SiteID = [1]
    SiteTypeID = 1
    AgentID = 1
    Debug = True
    custom_settings = {
        'COOKIES_ENABLED': True,
        'COOKIES_DEBUG': True,
        'DOWNLOADER_MIDDLEWARES': {
            'NFLScrape.middlewares.ProxyMiddleware': None
        }
    }

    def start_requests(self):
        url = 'http://www.nfl.com/stats/categorystats?tabSeq=0&statisticCategory=PASSING&conference=null&season=2018&seasonType=REG&d-447263-s=PASSING_YARDS&d-447263-o=2&d-447263-n=1'
        headers = {
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'http://www.nfl.com/stats/player',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse_request(self, response):
        content = (response.body_as_unicode().encode('cp850', 'replace').decode('cp850'))
        print(content)

    def get_stats(self, data):
        site = NFLScrapeItem(SiteID=self.SiteID[0], AgentID=self.AgentID)
        try:
            site['First']
        except TypeError:
            self.logger.info("Error: %s", site.items())
        return site
