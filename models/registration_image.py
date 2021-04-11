
from peewee import *

from .base_model import BaseModel

class RegistrationImage(BaseModel):
    id = PrimaryKeyField(null=False)
    registration_id = int
    image_name = CharField()
    # features = Byte

    class Meta:
        db_table = 'registration_image'


async def create_registration_image(registration_id: int, image_name: str):
    regis_img_object = RegistrationImage(
        registration_id = registration_id,
        image_name = image_name,
    )
    regis_img_object.save()
    return regis_img_object


def get_regis_img(regis_id: int):
    return RegistrationImage.filter(RegistrationImage.registration_id == regis_id).first()


def delete_contact(regis_id: int):
    return RegistrationImage.delete().where(RegistrationImage.registration_id == regis_id).execute()