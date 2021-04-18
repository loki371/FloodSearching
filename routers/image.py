from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile

from services import jwt
from models import registration_image, registration

from jose import JWTError
from services import cv_image

router_images = APIRouter(
    prefix="/pythonService/registrations/images",
    tags=["searching"]
)

@router_images.post("/{registrationId}", summary="Save image of registration to Server", description="Return true if we can save it, else false" )
async def saveImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None),
        image: UploadFile = File(...)
    ):

    print("Registration Id = ", registrationId)
    print("token = ", Authorization)

    username = None
    try:
        username = jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

    registration_record = registration.get_regis(registrationId)
    if (registration_record is None):
        raise HTTPException(status_code=404, detail="registration is not found")

    print(f'username = {username} & createdBy = {registration_record.create_by_username}')
    if (registration_record.create_by_username != username):
        raise HTTPException(status_code=405, detail="this registration is not belong to you")

    registration_image.delete_regis_img(registrationId)

    file_tail = image.filename.split('.')[-1]
    image_name = str(registrationId) + "." + file_tail
    image_location = f"images/{image_name}"
    
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())

    image_encoding = cv_image.encode_image(image_location)
    str_arr = cv_image.convert_array_to_str(image_encoding)
    registration_image.create_registration_image(registrationId, image_name, str_arr)

    return [{'status': 'OK'}]

@router_images.get("/{registrationId}", summary="Save image of registration to Server", description="Return true if we can save it, else false" )
async def getImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None)
    ):
    try:
        jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

    regis_img_record = registration_image.get_regis_img(registrationId)

    image_name = str(regis_img_record.image_name)
    image_location = f"images/{image_name}"
    image_like = open(image_location, mode="rb")

    if (regis_img_record is not None):
        print("imageName =  ", regis_img_record.image_name)
        registration_image.delete_regis_img(registrationId)

    return StreamingResponse(image_like, media_type="image")