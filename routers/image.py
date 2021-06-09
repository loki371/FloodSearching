from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile, HTTPException

from services import jwt
from models import registration_image, registration

from jose import JWTError
from services import search_image

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

    delete_regis_img_and_save_and_extract_feature_img(registrationId, image)

    return [{'status': 'OK'}]

@router_images.get("/{registrationId}", summary="Get image of registration to Server", description="Return true if we can save it, else false" )
async def getImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None)
    ):
    
    try:
        jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

    regis_img_record = registration_image.get_regis_img(registrationId)

    if (regis_img_record is not None):
        
        print("imageName =  ", regis_img_record['image_name'])

        image_name = regis_img_record['image_name']
        image_location = f"images/{image_name}"

        return [{"url": image_location}]

    else:
        raise HTTPException(status_code=404, detail="Item not found")


@router_images.get("/{registrationIds}", summary="Get List image of registration to Server", description="Return true if we can save it, else false" )
async def getImages(
        registrationIds: str, 
        Authorization: Optional[str] = Header(None)
    ):
    
    try:
        jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

    listRegisId = registrationIds.split(".")
    listRegisIdInt = [int(numeric_string) for numeric_string in listRegisId]
    listResult = {}

    for regisIdInt in listRegisIdInt:
        regis_img_record = registration_image.get_regis_img(regisIdInt)

        if (regis_img_record is not None):

            print("imageName =  ", regis_img_record['image_name'])
            image_name = regis_img_record['image_name']
            image_location = f"images/{image_name}"
            listResult[regisIdInt] = image_location

        else:
            listResult[regisIdInt] = ""

    return [{"regidId-url":listResult}]



# ------------------------------------------------------------------------------
# Utilities function

def delete_regis_img_and_save_and_extract_feature_img(registrationId, image):
    registration_image.delete_regis_img(registrationId)

    file_tail = image.filename.split('.')[-1]
    image_name = str(registrationId) + "." + file_tail
    image_location = f"images/{image_name}"
    
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())
    
    image_encoding = search_image.encode_image(image_location)
    registration_image.create_registration_image(registrationId, image_name, image_encoding)

    print("everything in here is so ok")