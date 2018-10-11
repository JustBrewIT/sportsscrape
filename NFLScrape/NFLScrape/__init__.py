import hashlib
import logging
from datetime import datetime
import re
import unidecode
import scrapy
# import NFLScrape.util
from NFLScrape import GetJobHistoryID
from NFLScrape.items import NFLScrapeItem
from NFLScrape.writeLog import writeLog
from NFLScrape.xmlGen import exportXML
from NFLScrape.csvGen import exportCSV
from NFLScrape.charFormat import format_string


class NFLSpider(scrapy.Spider):
    name = None
    SiteID = []
    SiteNames = []
    SiteTypeID = None
    SiteParentID = None
    AgentID = None
    NFLData = []
    NFLDataIDs = set()
    Duplicates = 0
    StartDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    FinishDatetime = None
    TestURL = ''
    RequestFailed = False
    Debug = True


    def start_requests(self):
        pass

    def parse(self, response):
        before = len(self.NFLData)
        befored = self.Duplicates
        self.parse_request(response)
        scraped = len(self.NFLData) - before
        afterd = self.Duplicates - befored

        if self.RequestFailed:
            self.logger.info(f'{response.url}: Failed. Retrying.')
            self.RequestFailed = False
            yield response.Request

        self.logger.info("{2}: Scraped {0} new NFLData! ({1} duplicates)".format(scraped, afterd, response.url))

    def parse_request(self, response):
        raise NotImplementedError

    def closed(self, reason):
        if len(self.NFLData) > 0:
            # self.FinishDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug("Scraped {0} total records!".format(len(self.NFLData)))
            for n, site_id in enumerate(self.SiteID):
                temp = []
                for item in self.NFLData:
                    print(item)
                    if item.get('SiteID') == site_id:
                        temp.append(item)
                logging.debug("Scraped {0} records for {1}!".format(len(temp), self.SiteNames[n]))
                # if self.settings['STATUS'] == 'DEV':
                exportCSV(site_id, self.AgentID, self.SiteNames[n], temp)
                # if self.settings['STATUS'] == 'PROD':
                # job_history_id = GetJobHistoryID(target_id)m
                # if job_history_id > 0:
                #     exportXML(self.NFLData[n], self.AgentID, target_id, job_history_id, temp, self.Debug)
                # if not self.Debug and job_history_id > 0:
                #     writeLog(site_id, self.AgentID, self.StartDatetime, self.FinishDatetime, job_history_id, len(temp))
            logging.debug('Spider closed: %s', self.name)
            logging.debug("Removed {0} duplicates!".format(self.Duplicates))

        else:
            logging.debug('Scraped nothing. Fail')

    def add_data(self, data):
        if data is None:
            return 0
        data = {k: format_string(v) for k, v in data.items()}
        # key = [i for n, i in enumerate(data) if i not in data[n + 1:]]
        key = str(data.get('FirstName', '') + data.get('LastName', '') + data.get('TeamName', ''))
        if key in self.NFLDataIDs:
            self.Duplicates += 1
        else:
            self.NFLDataIDs.add(key)
            self.NFLData.append(data)



