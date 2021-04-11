from typing import Optional

from fastapi import APIRouter, Header, File, UploadFile

router_images = APIRouter(
    prefix="/pythonService/registrations/images",
    tags=["images"]
)

@router_images.post("/{registrationId}", summary="Save image of registration to Server", description="Return true if we can save it, else false" )
async def get_contacts(
        registrationId: int, 
        Authorization: Optional[str] = Header(None),
        image: UploadFile = File(...)
    ):
    file_tail = image.filename.split('.')[-1]
    image_name = str(registrationId) + "." + file_tail
    image_location = f"images/{image_name}"
    print("registrationId = ", registrationId, " imageName = ", image_name, " authorization = ", Authorization)
    with open(image_location, "wb+") as file_object:
        file_object.write(image.file.read())
    return [{'status': 'OK'}]