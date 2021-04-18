from typing import Optional
from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Header, File, UploadFile

from services import jwt
from models import registration_image, registration

from jose import JWTError
from services.id_generator import generate
import os

router_images = APIRouter(
    prefix="/pythonService/registrations/searching",
    tags=["images"]
)

@router_images.get("/", summary="Search registration", description="Return list of similar registration" )
async def searchImage(
        registrationId: int, 
        Authorization: Optional[str] = Header(None),
        image: UploadFile = File(...),

        name: str,
        longitude: float,
        latitude: float,
        num_person: int,
        ward_id: int,
        phone: str,

    ):

    try:
        jwt.extract_token(Authorization)
    except JWTError:
        raise HTTPException(status_code=401, detail="token is not valid")

    print("searchImage: request info:\n "
        + " - name = " + name + "\n"
        + " - longitude = " + longitude + "\n"
        + " - latitude = " + latitude + "\n"
        + " - num_person = " + num_person + "\n"
        + " - ward_id = " + ward_id + "\n"
        + " - phone = " + phone)

    # save image to server
    id_image = generate()
    file_tail = image.filename.split('.')[-1]
    image_name = str(id_image) + file_tail
    image_location = f"temp_img/{image_name}"
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())

    # delete image
    os.remove(image_location)

    return [{'status': 'token is not valid'}]