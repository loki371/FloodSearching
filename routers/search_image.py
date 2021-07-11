from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile, HTTPException
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

THRESHOLD_DISTANCE = 500

@router_searching.post("/image/{name};{longitude};{latitude};{num_person};{ward_id};{phone}", description="Return list of similar registration")
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
        try:
            unknown_encoding = search_image.encode_image(image_location)
        except:
            print("no face in image")
            raise HTTPException(status_code=400, detail="image does not have face")

        # delete image
        search_image.remove_image(image_location)

    # load from DB
    registration_list = registration.find_by_ward_id(ward_id)

    # prepare for searching
    size_registration_list = len(registration_list)
    info_regis = []
    url_list = []
    differ_point = []

    # calculate distance base GPS
    distance_point = []
    for i in range(size_registration_list):
        info_regis.append(registration_list[i])

        distance_point.append(search_gps.get_distance(
            longitude, 
            latitude, 
            registration_list[i].longitude, 
            registration_list[i].latitude))

        differ_point.append(distance_point[i] * 1000)

    # remove distance > 500m
    for i in range(size_registration_list-1, -1, -1):
        if (distance_point[i] > THRESHOLD_DISTANCE):
            info_regis.pop(i)
            differ_point.pop(i)

    # calculate point base name and image
    for i in range(len(info_regis)):

        differ_point[i] += search_name.get_distance(info_regis[i].name, name)

        regis_img = registration_image.get_regis_img(info_regis[i].id)
        if regis_img == None or regis_img['features'] == None:
            print("this regis do not have image id = ", info_regis[i])
            differ_point[i] += search_image.getMaxPointImg()
            url_list.append("")
            continue

        print("imageName =  ", regis_img['image_name'])
        image_name = regis_img['image_name']
        image_location = f"images/{image_name}"
        url_list.append(image_location)

        if (unknown_encoding != None):
            differ_point[i] += search_image.get_distance(regis_img, unknown_encoding)
        else:
            differ_point[i] += search_image.getMaxPointImg()

    print('\n')

    differ_point_2 = {}
    info_regis_2 = {}
    url_list_2 = {}

    for i in range(len(differ_point)) :
        differ_point_2[i] = differ_point[i]
        info_regis_2[i] = info_regis[i]
        url_list_2[i] = url_list[i]

    print("\ndifferPoint : ", differ_point_2)
    print("\nregistrationList: ", info_regis_2)
    print("\nurl List", url_list_2)

    return [{'differ_point': differ_point_2, 'registrations' : info_regis_2, 'url_list': url_list_2}]

@router_searching.post("/noImage/{name};{longitude};{latitude};{num_person};{ward_id};{phone}", description="Return list of similar registration")
async def searchImage(
        Authorization: Optional[str] = Header(None),
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
        + f' - phone = {phone}')

    # load from DB
    registration_list = registration.find_by_ward_id(ward_id)

    # prepare for searching
    size_registration_list = len(registration_list)
    info_regis = []
    url_list = []
    differ_point = []

    # calculate distance base GPS
    print("regisList = ", registration_list)
    print("sizeRegisList = ", size_registration_list)
    distance_point = []
    for i in range(size_registration_list):
        info_regis.append(registration_list[i])

        distance_point.append(search_gps.get_distance(
            longitude, 
            latitude, 
            registration_list[i].longitude, 
            registration_list[i].latitude))

        differ_point.append(distance_point[i] * 1000)

    # remove distance > 500m
    for i in range(size_registration_list-1, -1, -1):
        if (distance_point[i] > THRESHOLD_DISTANCE):
            info_regis.pop(i)
            differ_point.pop(i)

    # calculate point base name and image
    for i in range(len(info_regis)):

        differ_point[i] += search_name.get_distance(info_regis[i].name, name)

        differ_point[i] += search_image.getMaxPointImg()

        regis_img = registration_image.get_regis_img(info_regis[i].id)
        if regis_img == None or regis_img['features'] == None:
            print("this regis do not have image id = ", info_regis[i].id)
            url_list.append("")
            continue

        print("imageName =  ", regis_img['image_name'])
        image_name = regis_img['image_name']
        image_location = f"images/{image_name}"
        url_list.append(image_location)

    print('\n len(differ_list) = ', len(differ_point))
    
    differ_point_2 = {}
    info_regis_2 = {}
    url_list_2 = {}

    for i in range(len(differ_point)) :
        differ_point_2[i] = differ_point[i]
        info_regis_2[i] = info_regis[i]
        url_list_2[i] = url_list[i]

    print("\ndifferPoint : ", differ_point_2)
    print("\nregistrationList: ", info_regis_2)
    print("\nurl List", url_list_2)

    return [{'differ_point': differ_point_2, 'registrations' : info_regis_2, 'url_list': url_list_2}]
