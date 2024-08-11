from fastapi import FastAPI, HTTPException, Response, UploadFile, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Annotated
# from io import BytesIO
# from PIL import Image
from mangum import Mangum

class OutputModel(BaseModel):
    preprocessed_image: str
    output_image: str
    total: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def hello_world():
    return {"hello": "world"}


handler = Mangum(app)
