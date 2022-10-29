from peewee import *

class AttckApt(Model):
    apt_id = AutoField(index=True,primary_key=True)
    apt_name = CharField()
    apt_hit_node = CharField()
    apt_percent = FloatField()
    apt_hit_tactics = CharField()

    class Meta:
        db_table = 'attckapt'

