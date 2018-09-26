import logging
import pyodbc


def writeLog(SiteID, SiteParentID, AgentID, StartDatetime, FinishDatetime, JobHistoryID):
    try:
        conn_str = (
            r'Driver={ODBC Driver 13 for SQL Server};'
            r'Server=DESKTOP-79VFTUR\SQLEXPRESS;'
            r'Trusted_Connection=yes;'
        )
        logging.debug("Connecting")
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        logging.debug("Connected")

        JobQuery = (
        "EXEC [SportsScrape].[dbo].[NFLScrape_uspJobHistory] @SiteID = %s, @SiteParentID = %s, @AgentID = %s, @StartDatetime = '%s', @FinishDatetime = '%s', @JobHistoryID = %s"
        % (SiteID, SiteParentID, AgentID, StartDatetime, FinishDatetime, JobHistoryID))

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

