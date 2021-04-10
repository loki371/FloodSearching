from fastapi import FastAPI
from db.database import *

app = FastAPI()

@app.on_event("startup")
async def startup():
    if conn.is_closed():
        conn.connect()
        
@app.on_event("shutdown")
async def shutdown():
    print("Closing...")
    if not conn.is_closed():
        conn.close()