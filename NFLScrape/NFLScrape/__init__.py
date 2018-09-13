import hashlib
import logging
from datetime import datetime
import re
import unidecode
import scrapy
from .DelBadChars import stripBadChars, StateToStateCode
from RetailScrape.GetJobHistoryID import GetJobHistoryID
from RetailScrape.URLBuilder import build_urls
from RetailScrape.items import RetailScrapeItem
from RetailScrape.writeLog import writeLog
from RetailScrape.xmlGen import exportXML
from RetailScrape.csvGen import exportCSV
from RetailScrape.addressValidation import validate
from RetailScrape.DelBadChars import get_us_states, StateToStateCode, stripBadChars, get_ca_states
from RetailScrape.util import convert_headers


class RetailSpider(scrapy.Spider):
    name = None
    ScraperTargetID = []
    AgentID = None
    LocationIDs = set()
    Locations = []
    Brands = []
    Duplicates = 0
    AgentStartTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    AgentEndTime = None
    Debug = True
    TestURL = ''
    RequestFailed = False
#    handle_httpstatus_list = [402]

    def start_requests(self):
        pass

    def parse(self, response):
        before = len(self.Locations)
        befored = self.Duplicates

        self.parse_request(response)
        scraped = len(self.Locations) - before
        afterd = self.Duplicates - befored

        if self.RequestFailed:
            self.logger.info(f'{response.url}: Failed. Retrying.')
            self.RequestFailed = False
            yield response.Request

        self.logger.info("{2}: Scraped {0} new locations! ({1} duplicates)".format(scraped, afterd, response.url))

    def parse_request(self, response):
        raise NotImplementedError

    def closed(self, reason):
        if len(self.Locations) > 0:
            self.AgentEndTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            logging.debug("Scraped {0} total locations!".format(len(self.Locations)))
            for n, target_id in enumerate(self.ScraperTargetID):
                temp = []
                for loc in self.Locations:
                    if loc.get('ScraperTargetID') == target_id:
                        temp.append(loc)
                logging.debug("Scraped {0} locations for {1}!".format(len(temp), self.Brands[n]))

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

        def format_pnumber(input_string):
            if input_string is None:
                return
            input_string = str(input_string)
            input_string = str(re.sub(r'(%..)', '', input_string)).encode("utf-8").decode("utf-8")
            input_string = unidecode.unidecode(input_string)
            return str(re.sub(r'[^0-9]', '', input_string)).encode("utf-8").decode("utf-8")

        if data is None:
            return 0

        if data.get('Street'):
            data['Street'] = format_string(data.get('Street')).encode("utf-8", "replace").decode("utf-8").strip()[:200]
        else:
            return 0
        if '-' in str(data.get('Zip')):
            data['Zip'] = str(data.get('Zip'))[:str(data.get('Zip')).find('-')].strip()[:9]
        if data.get('City'):
            data['City'] = format_string(data.get('City')).encode("utf-8", "replace").decode("utf-8").strip()[:100]
        if data.get('PhoneNumber'):
            data['PhoneNumber'] = format_pnumber(data.get('PhoneNumber'))[:15]

        address = ''
        if data.get('Country') in ['UK', 'GBR']:
            addresstypes = ['City', 'State', 'Zip']
            atcount = 0
            for at in addresstypes:
                if data.get(at):
                    atcount = atcount + 1
            if atcount > 1:
                try:
                    address = str(data.get('ScraperTargetID')) + ' ' + data.get('Street') + ' ' + data.get('City', '') + ' ' + data.get('State', '') + ' ' + data.get('Zip', '')
                except TypeError as e:
                    print(f'Address compile fail: {data}')
        else:
            if data.get('State'):
                state = StateToStateCode(format_string(data.get('State'))).encode("utf-8", "replace").strip().decode(
                    "utf-8")
                if len(state) > 2:
                    data['State'] = ''.join(item[0].upper() for item in data.get('State').split())
                else:
                    data['State'] = state
            if not (data.get('Street') and data.get('City') and data.get('State') and data.get('Zip')):
                print('needs address validation')
                data = validate(data)
            try:
                address = str(data.get('ScraperTargetID')) + ' ' + data.get('Street') + ' ' + data.get('City') + ' ' + data.get('State')
            except TypeError as e:
                print(f'Address compile fail: {data}')
        if address == '':
            return 0

        hash_object = hashlib.md5(address.encode("utf-8"))
        hash_id = hash_object.hexdigest()
        if hash_id in self.LocationIDs:
            self.Duplicates += 1
        else:
            self.LocationIDs.add(hash_id)
            self.Locations.append(data)



