from fastapi import FastAPI
from db.mysql import *
from routers import image

app = FastAPI()

app.include_router(image.router_images)

@app.on_event("startup")
async def startup():
    if conn.is_closed():
        conn.connect()
        
@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()