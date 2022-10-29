from peewee import *
from model import AttckApt


attckdb = MySQLDatabase("attck", autorollback=True, user='attck',password="sgcc.com", host='192.168.1.112', port=3306)

class DBInstance:
    def __init__(self) -> None:
        self.conn = attckdb.connect()
        attckdb.bind([AttckApt])
        # attckdb.create_tables(apt.AttckApt)
    
    def create_table_apt(self):
        AttckApt.create_table()

