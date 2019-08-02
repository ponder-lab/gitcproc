import sys, os
#import psycopg2
import logging
import codecs

sys.path.append("../util")

from DatabaseCon import DatabaseCon
from Config import Config
import Util


class dumpLogs:

    def __init__(self, password, c_info):
        self.config_info = c_info
        self.cfg = Config(self.config_info.CONFIG)
        self.dbPass = password
        self.connectDb()
        #self.cleanDb()

    @staticmethod
    def getFullTitleString(keywordDictionary):
        '''
        Create a string specifying not only the database column names
        but also their types.  This is used when automatically creating
        the database table.
        '''

        dictStr = "(project character varying(500), sha text, language character varying(500)," + \
            " file_name text, is_test boolean, method_name text"
        for key, value in keywordDictionary.iteritems():
            dictStr= dictStr+", "+ str(key).replace(" ", "_").replace("(", "_").replace(")", "_").lower() + \
                " integer" #ToStr will add ' around the strings...

        dictStr += ", total_adds integer, total_dels integer, warning_alert boolean)"

        return dictStr

    def connectDb(self):
        self.db_config = self.cfg.ConfigSectionMap("Database")
        logging.debug("Database configuration = %r\n", self.db_config)
        self.dbCon = DatabaseCon(self.db_config['database'], self.db_config['user'], \
                                 self.db_config['host'], self.db_config['port'], \
                                 self.dbPass)


    def cleanDb(self):

        schema = self.db_config['schema']
        response = 'y' # raw_input("Deleting database %s ?" % (self.db_config['schema']))

        schema = self.db_config['schema']
        tables = []
        tables.append(schema + "." + self.db_config['table_method_detail'])
        tables.append(schema + "." + self.db_config['table_change_summary'])

        if response.lower().startswith('y'):
            for table in tables:
                print("Deleting table %r \n" % table)
                sql_command = "DELETE FROM " + table
                self.dbCon.insert(sql_command)

        self.dbCon.commit()


    def close(self):
        self.dbCon.commit()
        self.dbCon.close()

     #TODO: Improve security here for possible injections?
    def createSummaryTable(self):
        schema = self.db_config['schema']
        table = schema + "." + self.db_config['table_change_summary']
        user = self.db_config['user']

        sql_command = "CREATE TABLE IF NOT EXISTS " + table + " (project character varying(500) NOT NULL," + \
            " sha text NOT NULL, author character varying(500), author_email character varying(500)," + \
            " commit_date date, is_bug boolean,"+ \
            " CONSTRAINT change_summary_pkey PRIMARY KEY (project, sha)) WITH (OIDS=FALSE);"
        self.dbCon.create(sql_command)
        #self.dbCon.create("ALTER TABLE " + table + " OWNER TO " + user + ";")
        #self.dbCon.create("GRANT ALL ON TABLE " + table + " TO " + user + ";")

    def createMethodChangesTable(self, titleString):
        schema = self.db_config['schema']
        table = schema + "." + self.db_config['table_method_detail']
        user = self.db_config['user']

        sql_command = "CREATE TABLE IF NOT EXISTS " + table + titleString + " WITH (OIDS=FALSE);"
        self.dbCon.create(sql_command)
        #self.dbCon.create("ALTER TABLE " + table + " OWNER TO " + user + ";")
        #self.dbCon.create("GRANT ALL ON TABLE " + table + " TO " + user + ";")


    def dumpSummary(self, summaryStr):

        schema = self.db_config['schema']
        table = schema + "." + self.db_config['table_change_summary']

        sql_command = "INSERT INTO " + table + \
                      "(project, sha, author, author_email, commit_date, is_bug)" + \
                      " VALUES (" + summaryStr + ")"

        #print sql_command
        self.dbCon.insert(sql_command)
        #self.dbCon.commit()

    def dumpMethodChanges(self, methodChange, titleString):

        schema = self.db_config['schema']
        table = schema + "." + self.db_config['table_method_detail']

        #sql_command = "INSERT INTO " + table + \
        #            "(project, sha, language, file_name, is_test, method_name, assertion_add, " + \
        #            "assertion_del, total_add, total_del)" + \
        #            "VALUES (" + methodChange + ")"

        sql_command = "INSERT INTO " + table + titleString + " VALUES (" + methodChange + ")"

        if(self.config_info.DEBUG):
            print(sql_command)

        self.dbCon.insert(sql_command)
        #self.dbCon.commit()


