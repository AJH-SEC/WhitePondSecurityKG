from peewee import *
from model import AttckApt


attckdb = MySQLDatabase("attck", autorollback=True, user='attck',password="", host='', port=3306)

class DBInstance:
    def __init__(self) -> None:
        self.conn = attckdb.connect()
        attckdb.bind([AttckApt])
        # attckdb.create_tables(apt.AttckApt)
    
    def create_table_apt(self):
        AttckApt.create_table()

