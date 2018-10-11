import os
import csv
import logging
from pathlib import Path
from time import strftime


def exportCSV(SiteID, AgentID, SiteName, data):
    ScrapeFolder = os.path.dirname(os.getcwd())
    while Path(os.path.join(ScrapeFolder, "NFLScrape")).exists():
        ScrapeFolder = os.path.join(ScrapeFolder,"NFLScrape")
    ScrapeFolder = os.path.join(ScrapeFolder, "Output", SiteName)

    if not os.path.exists(ScrapeFolder):
        os.makedirs(ScrapeFolder)

    with open(os.path.join(ScrapeFolder, "%s_%s.csv" % (SiteName, strftime("%Y%m%d"))), 'w', newline='',
              encoding='UTF-8', errors='replace') as csvOutput:
        all_keys = set().union(*(d.keys() for d in data))
        try:
            writer = csv.DictWriter(csvOutput, fieldnames=all_keys)
            writer.writeheader()
            for x in data:
                writer.writerow(x)
        except IndexError:
            pass
    return 0
