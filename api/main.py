from fastapi import FastAPI
from api.database import engine
from api import models

from api.routers import auth, other

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(router=auth.router)
app.include_router(router=other.router)

