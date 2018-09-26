import pyodbc
import logging


def GetJobHistoryID(JobHistoryID):

    try:
        conn_str = (
            r'Driver={ODBC Driver 13 for SQL Server};'
            r'Server=DESKTOP-79VFTUR\SQLEXPRESS;'
            r'Trusted_Connection=yes;'
            )
        cnxn = pyodbc.connect(conn_str)
        cursor = cnxn.cursor()
        JobHistoryID = ""
        JobQuery = (
            'SELECT MAX([JobHistoryID]) + 1 as [JobHistoryID]'
            'FROM [SportsScrape].[dbo].[JobHistory]'
            'WHERE [JobHistoryID] = %s'
            % JobHistoryID
            )
        cursor.execute(JobQuery)
        row = cursor.fetchone()
        while row:
            JobHistoryID = row[0]
            row = cursor.fetchone()

        cnxn.close()
        if JobHistoryID is None:
            JobHistoryID = 1
        return(JobHistoryID)
    except pyodbc.OperationalError:
        logging.debug('Cannot connect to DB for JobHistoryID')
        return -1