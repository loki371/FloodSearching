from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile

from services import jwt
from models import registration_image, registration

from jose import JWTError

router_images = APIRouter(
    prefix="/pythonService/registrations/images",
    tags=["images"]
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
        return [{'status': 'token is not valid'}]

    registration_record = registration.get_regis(registrationId)
    if (registration_record is None):
        return [{'status': 'not found'}]

    print(f'username = {username} & createdBy = {registration_record.create_by_username}')
    if (registration_record.create_by_username != username):
        return [{'status': 'this registration not belong to you'}]

    registration_image.delete_regis_img(registrationId)

    file_tail = image.filename.split('.')[-1]
    image_name = str(registrationId) + "." + file_tail
    image_location = f"images/{image_name}"
    
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())

    registration_image.create_registration_image(registrationId, image_name)

    return [{'status': 'OK'}]

@router_images.get("/{registrationId}", summary="Save image of registration to Server", description="Return true if we can save it, else false" )
async def getImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None)
    ):
    try:
        jwt.extract_token(Authorization)
    except JWTError:
        return [{'status': 'token is not valid'}]

    regis_img_record = registration_image.get_regis_img(registrationId)

    image_name = str(regis_img_record.image_name)
    image_location = f"images/{image_name}"
    image_like = open(image_location, mode="rb")

    if (regis_img_record is not None):
        print("imageName =  ", regis_img_record.image_name)
        registration_image.delete_regis_img(registrationId)

    return StreamingResponse(image_like, media_type="image/jpeg")