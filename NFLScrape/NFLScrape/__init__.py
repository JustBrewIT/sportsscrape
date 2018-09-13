import hashlib
import logging
from datetime import datetime
import re
import unidecode
import scrapy
from NFLScrape.NFLScrape.charFormat import stripBadChars
from NFLScrape.NFLScrape.items import NFLScrapeItem
#from NFLScrape.NFLScrape.writeLog import writeLog
from NFLScrape.NFLScrape.xmlGen import exportXML
from NFLScrape.NFLScrape.csvGen import exportCSV
from NFLScrape.NFLScrape.util import convert_headers



class NFLSpider(scrapy.Spider):
    name = None
    SiteID = []
    AgentID = None
    LocationIDs = set()
    nfldata = []
    Brands = []
    Duplicates = 0
    AgentStartTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    AgentEndTime = None
    TestURL = ''
    RequestFailed = False
#    handle_httpstatus_list = [402]

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
            self.AgentEndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug("Scraped {0} total nfldata!".format(len(self.nfldata)))
            for n, target_id in enumerate(self.SiteID):
                temp = []
                for loc in self.nfldata:
                    if loc.get('SiteID') == target_id:
                        temp.append(loc)
                logging.debug("Scraped {0} nfldata for {1}!".format(len(temp), self.Brands[n]))

                if self.settings['STATUS'] == 'DEV':
                    exportCSV(self.Brands[n], self.AgentID, target_id, temp, self.Debug)
                if self.settings['STATUS'] == 'PROD':
                    job_history_id = GetJobHistoryID(target_id)
                    if job_history_id > 0:
                        exportXML(self.Brands[n], self.AgentID, target_id, job_history_id, temp, self.Debug)
                    if not self.Debug and job_history_id > 0:
                        writeLog(target_id, self.AgentID, self.AgentStartTime, self.AgentEndTime,
                                 job_history_id, len(temp))

            logging.debug('Spider closed: %s', self.name)
            logging.debug("Removed {0} duplicates!".format(self.Duplicates))

        else:
            logging.debug('Scraped nothing. Fail')

    def add_data(self, data):

        def format_string(input_string):
            if input_string is not None:
                input_string = unidecode.unidecode(input_string)
                input_string = input_string.replace('%20', ' ')
                input_string = input_string.replace('-', ' ')
                input_string = input_string.replace('_', ' ')
                bad_chars = ['#', '?', '&', ';', '(', ')', '$', '!', '<', '>']
                for x in bad_chars:
                    input_string = input_string.replace(x, '')
                return stripBadChars(input_string)

        if data is None:
            return 0
        hash_string = ''

        hash_object = hashlib.md5(hash_string.encode("utf-8"))
        hash_id = hash_object.hexdigest()
        if hash_id in self.SiteIDs:
            self.Duplicates += 1
        else:
            self.SiteIDs.add(hash_id)
            self.nfldata.append(data)



