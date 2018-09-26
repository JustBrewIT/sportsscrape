import scrapy
import hashlib
import logging
from datetime import datetime
import re
import unidecode
from NFLScrape.charFormat import format_string
from NFLScrape.GetJobHistoryID import GetJobHistoryID
from NFLScrape.items import NFLScrapeItem
from NFLScrape.writeLog import writeLog
from NFLScrape.xmlGen import exportXML
from NFLScrape.csvGen import exportCSV
from NFLScrape.util import convert_headers



class NFLSpider(scrapy.Spider):
    name = None
    SiteID = []
    SiteTypeID = None
    SiteParentID = ''
    AgentID = None
    nfldata = []
    Duplicates = 0
    # StartDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # FinishDatetime = None
    TestURL = ''
    RequestFailed = False
    Debug = True


    def start_requests(self):
        pass

    def parse(self, response):
        before = len(self.nfldata)
        befored = self.Duplicates
        self.parse_request(response)
        scraped = len(self.nfldata) - before
        afterd = self.Duplicates - befored

        if self.RequestFailed:
            self.logger.info(f'{response.url}: Failed. Retrying.')
            self.RequestFailed = False
            yield response.Request

        self.logger.info("{2}: Scraped {0} new nfldata! ({1} duplicates)".format(scraped, afterd, response.url))

    def parse_request(self, response):
        raise NotImplementedError

    def closed(self, reason):
        if len(self.nfldata) > 0:
            # self.FinishDatetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug("Scraped {0} total records!".format(len(self.nfldata)))
            for n, target_id in enumerate(self.SiteID):
                temp = []
                for item in self.nfldata:
                    if item.get('SiteID') == target_id:
                        temp.append(item)
                logging.debug("Scraped {0} nfldata for {1}!".format(len(temp), self.nfldata[n]))
                # if self.settings['STATUS'] == 'DEV':
                exportCSV(self.nfldata[n], self.AgentID, target_id, temp, self.Debug)
                # if self.settings['STATUS'] == 'PROD':
                # job_history_id = GetJobHistoryID(target_id)
                # if job_history_id > 0:
                #     exportXML(self.nfldata[n], self.AgentID, target_id, job_history_id, temp, self.Debug)
                # if not self.Debug and job_history_id > 0:
                #     writeLog(target_id, self.AgentID, self.FinishDatetime, self.FinishDatetime, job_history_id, len(temp))
            logging.debug('Spider closed: %s', self.name)
            logging.debug("Removed {0} duplicates!".format(self.Duplicates))

        else:
            logging.debug('Scraped nothing. Fail')

    def add_data(self, data):
        key = [i for n, i in enumerate(data) if i not in data[n + 1:]]
        if data is None:
            return 0
        if key in self.SiteID:
            self.Duplicates += 1
        else:
            self.SiteID.add(key)
            self.nfldata.append(data)



