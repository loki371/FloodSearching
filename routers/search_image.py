from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile
from pydantic import BaseModel, Field

from services import jwt
from models import registration_image, registration

from jose import JWTError
from services import id_generator, cv_image
import os

router_searching = APIRouter(
    prefix="/pythonService/registrations/searching",
    tags=["images"]
)

@router_searching.get("/{name};{longitude};{latitude};{num_person};{ward_id};{phone}", description="Return list of similar registration")
async def searchImage(
        Authorization: Optional[str] = Header(None),
        image: UploadFile = File(...),

        name: Optional[str] = "",
        longitude: Optional[float] = 0,
        latitude: Optional[float] = 0,
        num_person: Optional[int] = 0,
        ward_id: Optional[str] = 0,
        phone: Optional[str] = 0,
    ):

    # try:
    #     jwt.extract_token(Authorization)
    # except JWTError:
    #     raise HTTPException(status_code=401, detail="token is not valid")

    print("searchImage: request info:\n "
        + f' - name = {name}\n'
        + f' - longitude = {longitude}\n'
        + f' - latitude = {latitude}\n'
        + f' - num_person = {num_person}\n'
        + f' - ward_id = {ward_id}\n'
        + f' - phone = {phone}\n')

    # save image to server
    id_image = await id_generator.generate()

    file_tail = image.filename.split('.')[-1]
    image_name = str(id_image) + '.' + file_tail
    image_location = f"temp_img/{image_name}"
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())

    unknown_encoding = cv_image.encode_image(image_location)

    # delete image
    cv_image.remove_image(image_location)

    registration_list = registration.find_by_ward_id(ward_id)

    differ_point = {}
    size_registration_list = len(registration_list)
    info_regis = {}

    for i in range(size_registration_list):
        item_regis = {}
        item_regis['name'] = registration_list[i].name
        item_regis['ward_id'] = registration_list[i].ward_id
        info_regis[i] = item_regis

        regis_img = registration_image.get_regis_img(registration_list[i])
        
        if (regis_img == None):
            differ_point[i] = 1000
            continue

        if (regis_img.str_arr == None):
            differ_point[i] = 1000
            continue

        int_arr = cv_image.convert_str_to_arr(regis_img.str_arr)
        differ_point[i] = cv_image.verify(unknown_encoding, int_arr)['distance']

    return [{'differ_point': differ_point, 'registrations' : info_regis}]
