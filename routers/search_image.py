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

    try:
        jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

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

    registration_list = registration.find_by_ward_id(ward_id)
    registration_id_list = []
    for item in registration_list:
        registration_id_list.append(item.id)
    print("list regis id = ", registration_id_list)

    # delete image
    cv_image.remove_image(image_location)

    return [{'status': 'ok'}]