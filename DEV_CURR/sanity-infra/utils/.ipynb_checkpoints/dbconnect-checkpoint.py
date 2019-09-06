""" DB Connector util """

import mysql.connector as mdb
import sys
from utils.logger import Logger
from utils import constants

log = Logger(__name__)


class DBConnect:
    db_con = None
    cursor = None

    def __init__(self):
        """ get a mysql db connection """
        try:
            self.db_con = mdb.connect(host='{0}'.format(constants.DB_HOST), user='{0}'.format(constants.DB_USER),
                                      password="{0}".format(constants.DB_PASS), db='{0}'.format(constants.DB_NAME),
                                      use_pure=True)
            self.cursor = self.db_con.cursor()
        except Exception as e:
            log.error("execute Failure" + repr(e))
            sys.exit("db con failed")

    def close_connection(self):
        self.db_con.close()

    def execute(self, sql_cmd=None):
        """ mysql cmd """
        try:
            log.debug(sql_cmd)
            self.cursor.execute(sql_cmd)
            self.db_con.commit()
            return True
        except Exception as e:
            log.error("execute Failure" + repr(e))
            return False

    def fetch(self, sql_cmd=None, type=None):
        """
            Fetch from db --> args:
            sql_cmd = (SQL CMD TO FETCH)
            type = return type current options default,dict,named_tuple
        """
        log.debug(sql_cmd)
        connection = self.db_con
        # cursor = connection.cursor()
        if type is not None:
            if type == "_dict":
                cursor = connection.cursor(dictionary=True)
            elif type == "_tuple":
                cursor = connection.cursor(named_tuple=True)
        else:
            cursor = connection.cursor()
        cursor.execute(sql_cmd)
        rows = cursor.fetchall()
        return rows
