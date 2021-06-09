from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile
from numpy.core.fromnumeric import size
from pydantic import BaseModel, Field

from services import jwt
from models import registration_image, registration

from jose import JWTError
from services import id_generator, search_image, search_name, search_gps
import os

router_searching = APIRouter(
    prefix="/pythonService/registrations/searching",
    tags=["images"]
)

@router_searching.get("/{name};{longitude};{latitude};{num_person};{ward_id};{phone}", description="Return list of similar registration")
async def searchImage(
        Authorization: Optional[str] = Header(None),
        image: Optional[UploadFile] = File(...),

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

    print("searchImage: request info:\n"
        + f' - name = {name}\n'
        + f' - longitude = {longitude}\n'
        + f' - latitude = {latitude}\n'
        + f' - num_person = {num_person}\n'
        + f' - ward_id = {ward_id}\n'
        + f' - phone = {phone}\n'
        + f' - isFileNULL = {image == None}')

    # save image to server
    unknown_encoding = None
    if (image != None):
        id_image = await id_generator.generate()
        file_tail = image.filename.split('.')[-1]
        image_name = str(id_image) + '.' + file_tail
        image_location = f"temp_img/{image_name}"
        with open(image_location, "wb+") as file_object:
            file_object.write(image.file.read())

        # extra features of image
        unknown_encoding = search_image.encode_image(image_location)

        # delete image
        search_image.remove_image(image_location)

    # load from DB
    registration_list = registration.find_by_ward_id(ward_id)

    # prepare for searching
    differ_point = {}
    size_registration_list = len(registration_list)
    info_regis = {}
    url_list = {}

    # calculate point
    for i in range(size_registration_list):
        print('\n')
        # init item_regis and differ_point
        item_regis = registration_list[i]

        info_regis[i] = item_regis
        differ_point[i] = 0

        # calculate point by GPS
        differ_point[i] += search_gps.get_distance(
            longitude, 
            latitude, 
            registration_list[i].longitude, 
            registration_list[i].latitude)

        # calculate point by name
        differ_point[i] += search_name.get_distance(registration_list[i].name, name)

        # calculate point by image
        regis_img = registration_image.get_regis_img(registration_list[i].id)
        if regis_img == None or regis_img['features'] == None:
            differ_point[i] += 1000
            url_list[i] = ""
            continue

        print("imageName =  ", regis_img['image_name'])
        image_name = regis_img['image_name']
        image_location = f"images/{image_name}"
        url_list[i] = image_location

        differ_point[i] += search_image.get_distance(regis_img, unknown_encoding)

    print('\n')
    return [{'differ_point': differ_point, 'registrations' : info_regis, 'url_list': url_list}]
