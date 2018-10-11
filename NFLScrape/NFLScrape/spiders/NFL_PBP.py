import scrapy
import NFLScrape
from NFLScrape import NFLScrapeItem
import logging
import re
import json
import unidecode


class NFL(NFLScrape.NFLSpider):
    name = 'NFL_PBP'
    SiteID = [1]
    SiteNames = ['NFL_PBP']
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
        url = 'http://www.nfl.com/liveupdate/game-center/2018090600/2018090600_gtd.json?random=1538105660000'
        headers = {
            'DNT': '1',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36',
            'Accept': '*/*',
            'Referer': 'http://www.nfl.com/gamecenter/2018090600/2018/REG1/falcons@eagles',
            'X-Requested-With': 'XMLHttpRequest',
            'Connection': 'keep-alive',
        }
        yield scrapy.Request(url=url, headers=headers, callback=self.parse)

    def parse_request(self, response):
        k = None
        r = re.compile(r".*/(\d+)")
        url = response.url
        if r.match(url):
            k = r.findall(url)[0].strip()
        print(k)
        if k:
            content = (response.body_as_unicode().encode('cp850', 'replace').decode('cp850'))
            data = json.loads(content)
            data_team = {}
            data_team['HomeTeamName'] = data[k]['home']['abbr']
            data_team['AwayTeamName'] = data[k]['away']['abbr']
            data_team['AwayTeamName'] = data[k]['away']['abbr']


        #       self.add_data(self.get_stats(data, data_team))

    def get_stats(self, data, data_team):
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
