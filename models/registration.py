from peewee import *
from typing import Optional

from db.mysql import BaseModel

class Registration(BaseModel):
    name = CharField(45)
    longitude = FloatField 
    latitude = FloatField
    num_person = IntegerField
    ward_id = CharField(6)
    e_state = IntegerField
    saved_by_username = CharField(20)
    create_by_username = CharField(20)
    phone = CharField(255)

    class Meta:
        db_table = 'registrations'

def get_regis(regis_id: int):
    try:
        return Registration.select().where(Registration.id == regis_id).get()
    except RegistrationImage.DoesNotExist:
        return None


def find_by_ward_id(ward_id: int):
    try:
        return Registration.select().where(Registration.ward_id == ward_id).limit(100)
    except Registration.DoesNotExist:
        return None


def delete_regis(regis_id: int):
    try:
        return Registration.delete().where(Registration.id == regis_id).execute()
    except RegistrationImage.DoesNotExist:
        return None