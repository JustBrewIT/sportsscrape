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
    SiteNames = ['NFLOffense']
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
        # content = (response.body_as_unicode().encode('cp850', 'replace').decode('cp850'))
        for data in response.xpath('(//table[@id="result"]/tbody)[position() = last()]/tr'):
            self.add_data(self.get_stats(data))

    def get_stats(self, data):
        site = NFLScrapeItem(SiteID=self.SiteID[0], AgentID=self.AgentID)
        try:
            name = data.xpath('.//td[2]/a/text()').extract_first()
            try:
                site['FirstName'] = re.findall('(.*?)\s', name)[0]
                site['LastName'] = re.findall('.*?\s(.*)', name)[0]
            except IndexError:
                self.logger.info("Error: %s", site.items())
            site['TeamName'] = data.xpath('.//td[3]/a/text()').extract_first()
            site['PositionName'] = data.xpath('.//td[4]/text()').extract_first()
            site['Pass_Completions'] = data.xpath('.//td[5]/text()').extract_first()
            site['Pass_Attempts'] = data.xpath('.//td[6]/text()').extract_first()
            site['Pass_Yards'] = data.xpath('.//td[9]/text()').extract_first()
            site['Pass_Touchdowns'] = data.xpath('.//td[11]/text()').extract_first()
            site['Pass_Interceptions'] = data.xpath('.//td[12]/text()').extract_first()
            site['Pass_FirstDowns'] = data.xpath('.//td[13]/text()').extract_first()
            site['Pass_Long'] = data.xpath('.//td[15]/text()').extract_first()
            site['Pass_20'] = data.xpath('.//td[16]/text()').extract_first()
            site['Pass_40'] = data.xpath('.//td[17]/text()').extract_first()
            site['Pass_Sacks'] = data.xpath('.//td[18]/text()').extract_first()
            site['Pass_Rating'] = data.xpath('.//td[19]/text()').extract_first()
        except TypeError:
            self.logger.info("Error: %s", site.items())
        return site
