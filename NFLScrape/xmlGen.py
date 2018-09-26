import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from time import strftime

def exportXML(StoreName, AgentID, ScraperTargetID, ScraperJobHistoryID, scraped_data, debug):
    OutPutFolder = '\\\\dcfilprd100\\BrokerListingExtract-Prd\\Content Acquisition\\Scrape Outputs\\XML Exports\\'
    ScrapeFolder = os.path.dirname(os.getcwd())
    while Path(os.path.join(ScrapeFolder,"RetailScrape")).exists():
        ScrapeFolder = os.path.join(ScrapeFolder,"RetailScrape")
    ScrapeFolder = os.path.join(ScrapeFolder, "Output", StoreName)
    
    if not os.path.exists(ScrapeFolder):
        os.makedirs(ScrapeFolder)
    ExportedJobsDS = ET.Element("ExportedJobsDS ")
    ScraperTarget = ET.SubElement(ExportedJobsDS, "ScraperTarget")
    ET.SubElement(ScraperTarget, "ScraperTargetID").text = str(ScraperTargetID)
    ET.SubElement(ScraperTarget, "AgentID").text = str(AgentID)
    ET.SubElement(ScraperTarget, "TotalTargetObjects")
    ET.SubElement(ScraperTarget, "Priority")
    ET.SubElement(ScraperTarget, "WebAddress")
    ET.SubElement(ScraperTarget, "Comments")
    ET.SubElement(ScraperTarget, "CreatedDate")
    ET.SubElement(ScraperTarget, "UpdatedDate").text = str(datetime.now().isoformat())
    ET.SubElement(ScraperTarget, "ScraperTargetName").text = StoreName[:50]
    ET.SubElement(ScraperTarget, "ScraperTargetTypeId")
    ET.SubElement(ScraperTarget, "ScraperTargetStatusID")

    ScraperJobHistory = ET.SubElement(ExportedJobsDS, "ScraperJobHistory")
    ET.SubElement(ScraperJobHistory, "ScraperJobHistoryID").text = str(ScraperJobHistoryID)
    ET.SubElement(ScraperJobHistory, "ScraperScheduleID")
    ET.SubElement(ScraperJobHistory, "JobStatusID")
    ET.SubElement(ScraperJobHistory, "StartDate")
    ET.SubElement(ScraperJobHistory, "EndDate")
    ET.SubElement(ScraperJobHistory, "StoreCount").text = str(len(scraped_data))
    ET.SubElement(ScraperJobHistory, "WorkerProcessName")
    ET.SubElement(ScraperJobHistory, "CreatedDate").text = str(datetime.now().isoformat())
    ET.SubElement(ScraperJobHistory, "UpdatedDate").text = str(datetime.now().isoformat())


    for n,x in enumerate(scraped_data):
        ScraperTenantResult = ET.SubElement(ExportedJobsDS, "ScraperTenantResult")
        ET.SubElement(ScraperTenantResult, "ScraperTenantResultID").text = str(n+1)
        ET.SubElement(ScraperTenantResult, "ScraperTargetID").text = str(ScraperTargetID)
        if ScraperJobHistoryID is not None:
            ET.SubElement(ScraperTenantResult, "ScraperJobHistoryID").text = str(ScraperJobHistoryID)

        ET.SubElement(ScraperTenantResult, "TargetPropertyID")
        ET.SubElement(ScraperTenantResult, "StoreHours")
        ET.SubElement(ScraperTenantResult, "StoreFeatures")

        if x.get('Street') is not None:
            ET.SubElement(ScraperTenantResult, "Street1").text = formatString(x.get('Street')).strip()[:180]
        else:
            ET.SubElement(ScraperTenantResult, "Street").text

        ET.SubElement(ScraperTenantResult, "Street2").text

        if x.get('City') is not None:
            ET.SubElement(ScraperTenantResult, "City").text = formatString(x.get('City')).strip()[:50]
        else:
            ET.SubElement(ScraperTenantResult, "City").text

        if x.get('State') is not None:
            ET.SubElement(ScraperTenantResult, "State").text = formatString(StateToStateCode(x.get('State'))).strip()[:2]
        else:
            ET.SubElement(ScraperTenantResult, "State").text

        if x.get('Latitude') is not None:
            ET.SubElement(ScraperTenantResult, "Latitude").text = str(x.get('Latitude')).strip()[:50]
        else:
            ET.SubElement(ScraperTenantResult, "Latitude").text

        if x.get('Longitude') is not None:
            ET.SubElement(ScraperTenantResult, "Longitude").text = str(x.get('Longitude')).strip()[:50]
        else:
            ET.SubElement(ScraperTenantResult, "Longitude").text

        if x.get('Zip') is not None:
            ET.SubElement(ScraperTenantResult, "Zip").text = str(x.get('Zip'))[:9]
        else:
            ET.SubElement(ScraperTenantResult, "Zip").text

        if x.get('PhoneNumber') is not None:
            ET.SubElement(ScraperTenantResult, "Phone").text = str(re.sub(r'[^0-9]', '',
                                                                          str(x.get('PhoneNumber')))).strip()[:10]
        else:
            ET.SubElement(ScraperTenantResult, "Phone")

        ET.SubElement(ScraperTenantResult, "Note")
        ET.SubElement(ScraperTenantResult, "StoreWebAddress")
        ET.SubElement(ScraperTenantResult, "Location").text
        ET.SubElement(ScraperTenantResult, "CreatedDate").text = str(datetime.now().isoformat())
        ET.SubElement(ScraperTenantResult, "UpdatedDate").text = str(datetime.now().isoformat())
        ET.SubElement(ScraperTenantResult, "TargetObjectHash")
        if x.get('StoreName') is not None:
            ET.SubElement(ScraperTenantResult, "StoreName").text = str(x.get('StoreName')).strip()[:50]
        else:
            ET.SubElement(ScraperTenantResult, "StoreName").text = StoreName

    tree = ET.ElementTree(ExportedJobsDS)

    treeCopy = tree

    if not debug:
        try:
            tree.write(os.path.join(OutPutFolder,"%s_%s.xml" % (StoreName,strftime("%Y%m%d"))))
        except:
            print('Fileserver not available')

    treeCopy.write(os.path.join(ScrapeFolder, "%s_%s.xml" % (StoreName, strftime("%Y%m%d"))))

    return 0


def formatString(Input):
    if Input is not None:
        badChars = ['#', '?']
        for x in badChars:
            Input = Input.replace(x, '')
        return stripBadChars(Input)
