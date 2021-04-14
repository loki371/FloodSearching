#https://docs.peewee-orm.com/en/latest/peewee/quickstart.html#model-definition

from peewee import *
user = 'root'
password = 'Aa123456'
db_name = 'cuu_nan'

conn = MySQLDatabase(
    database= db_name, 
    user=user,
    password=password,
    host='localhost'
)
class BaseModel(Model):
    class Meta:
        database = conn