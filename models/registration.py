from peewee import *
from typing import Optional

from db.mysql import BaseModel

class Registration(BaseModel):
    name: str
    description: Optional[str] = None
    longitude: Optional[float] = None
    latitude: Optional[float] = None
    num_person: Optional[int] = None
    ward_id: Optional[str] = None
    e_state: Optional[int] = None
    saved_by_username: Optional[str] = None
    created_by_username: Optional[str] = None
    phone: Optional[str] = None

    class Meta:
        db_table = 'registrations'

def get_regis(regis_id: int):
    return Registration.filter(Registration.id == regis_id).first()


def delete_regis_img(regis_id: int):
    return Registration.delete().where(Registration.id == regis_id).execute()