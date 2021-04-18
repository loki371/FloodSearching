from peewee import *

from db.mysql import BaseModel

class RegistrationImage(BaseModel):
    id = IntegerField
    image_name = CharField(255)
    str_arr = TextField()

    class Meta:
        db_table = 'registration_image'

# RegistrationImage.create_table()

def create_registration_image(registration_id: int, image_name: str, str_arr: str):
    regis_img_object = RegistrationImage.create(
        image_name = image_name,
        id = registration_id,
        str_arr = str_arr
    )
    print(f'creating: id = {regis_img_object.id} imageName = {regis_img_object.image_name}')
    return regis_img_object


def get_regis_img(regis_id: int):
    try:
        return RegistrationImage.select().where(RegistrationImage.id == regis_id).get()
    except RegistrationImage.DoesNotExist:
        return None


def delete_regis_img(regis_id: int):
    try:
        return RegistrationImage.delete().where(RegistrationImage.id == regis_id).execute()
    except RegistrationImage.DoesNotExist:
        return None