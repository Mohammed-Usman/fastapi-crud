import time

import psycopg

from psycopg.rows import dict_row
from fastapi import FastAPI

from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

while True:
    try:
        conn = psycopg.connect(
            "host=localhost dbname=fastapi_crud user=postgres password=1234",
            row_factory=dict_row)

        cursor = conn.cursor()

        print("DB SUccess")

        break
    except Exception as e:
        print("DB connection failed")
        print("Error", e)
        time.sleep(2)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
