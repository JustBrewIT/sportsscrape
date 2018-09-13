import logging
import pyodbc


def writeLog(ScraperTargetID, AgentID, AgentStartTime, AgentEndTime, ScraperJobHistoryID, LocationsScraped):
    try:
        conn_str = (
            r'Driver={ODBC Driver 13 for SQL Server};'
            r'Server=DCSQLPRD104;'
            r'Trusted_Connection=yes;'
        )
        logging.debug("Connecting")
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        logging.debug("Connected")

        JobQuery = (
        "EXEC [ADC].[dbo].[HN_rptRetailScrapeAgentLogInsert] @TargetID = %s,@AgentID = %s,@AgentStartTime = '%s', @AgentEndTime = '%s', @JobHistoryID = %s, @LocationCount= %s"
        % (ScraperTargetID, AgentID, AgentStartTime, AgentEndTime, ScraperJobHistoryID, LocationsScraped))

        try:
            cursor.execute(JobQuery)
            cursor.commit()
            logging.debug('Wrote to log')
        except:
            logging.debug('Error writing to log: %s', JobQuery)

        cnxn.close()
    except pyodbc.OperationalError:
        logging.debug('Cannot connect to DB.')
    return ()

