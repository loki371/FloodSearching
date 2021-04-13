from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile

from services import jwt
from models import registration_image, registration

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
    jwt.extract_token(Authorization)

    registration_record = registration.get_regis(registrationId)
    if (registration_record is None):
        return [{'status': 'not found'}]

    print("regis_record ",registration_record)

    regis_img_record = registration_image.get_regis_img(registrationId)

    print("regis_img_record ",regis_img_record)

    file_tail = image.filename.split('.')[-1]
    image_name = str(registrationId) + "." + file_tail
    image_location = f"images/{image_name}"
    
    print("registrationId = ", registrationId, " imageName = ", image_name, " authorization = ", Authorization)
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())
    return [{'status': 'OK'}]

@router_images.get("/{registrationId}", summary="Save image of registration to Server", description="Return true if we can save it, else false" )
async def getImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None)
    ):
    # jwt.extract_token(Authorization)

    image_name = str(registrationId) + ".jpeg"
    image_location = f"images/{image_name}"
    image_like = open(image_location, mode="rb")
    return StreamingResponse(image_like, media_type="image/jpeg")