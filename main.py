from fastapi import FastAPI
from db.mysql import *
from routers import image, search_image
from deepface import DeepFace
import pathlib

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(image.router_images)
app.include_router(search_image.router_searching)


@app.on_event("startup")
async def startup():
    print(pathlib.Path(__file__).parent.absolute())

    if conn.is_closed():
        conn.connect()    
        
@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()


