'''
Created on Aug 7, 2017

@author: hnagarajan
'''

import os
import csv
import logging
from pathlib import Path
from time import strftime


def exportCSV(StoreName, AgentID, ScraperTargetID, scraped_data, debug):
    ScrapeFolder = os.path.dirname(os.getcwd())
    while Path(os.path.join(ScrapeFolder, "RetailScrape")).exists():
        ScrapeFolder = os.path.join(ScrapeFolder,"RetailScrape")
    ScrapeFolder = os.path.join(ScrapeFolder, "Output", StoreName)
    
    if not os.path.exists(ScrapeFolder):
        os.makedirs(ScrapeFolder)

    with open(os.path.join(ScrapeFolder, "%s_%s.csv" % (StoreName, strftime("%Y%m%d"))), 'w', newline='',
              encoding='UTF-8', errors='replace') as csvOutput:
        all_keys = set().union(*(d.keys() for d in scraped_data))
        try:
            writer = csv.DictWriter(csvOutput, fieldnames=all_keys)
            writer.writeheader()
            for x in scraped_data:
                writer.writerow(x)
        except IndexError:
            pass

    if debug is False:
        try:
            export_dir = '\\\\dcfilprd100\\BrokerListingExtract-Prd\\Content Acquisition\\Scrape Outputs\\'
            with open(os.path.join(export_dir, "%s_%s.csv" % (StoreName, strftime("%Y%m%d"))), 'w', newline='',
                      encoding='UTF-8', errors='replace') as export:
                all_keys = set().union(*(d.keys() for d in scraped_data))
                try:
                    writer = csv.DictWriter(export, fieldnames=all_keys)
                    writer.writeheader()
                    for x in scraped_data:
                        writer.writerow(x)
                except IndexError:
                    pass
        except Error:
            logging.debug('Could not export to dcfilprd100')
    return 0
