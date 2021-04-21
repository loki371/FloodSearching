from peewee import *

from db.mongo import db

def create_registration_image(registration_id: int, image_name: str, float_arr):
    regis_img_object = {
        'regis_id': registration_id,
        'image_name': image_name,
        'features': float_arr
    }

    id_object = db.registration_image.insert_one(regis_img_object)
    print(f'creating: idObject = {id_object}')
    return regis_img_object


def get_regis_img(regis_id: int):
    try:
        print('get_regis_img: regis_id = ', regis_id)
        return db.registration_image.find_one({'regis_id' : regis_id})
    except:
        print('get_regis_img: exception')
        return None


def delete_regis_img(regis_id: int):
    db.registration_image.delete_one({'regis_id' : regis_id})