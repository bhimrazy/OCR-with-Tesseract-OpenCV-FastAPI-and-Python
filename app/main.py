from typing import Optional

from fastapi import FastAPI, status, File, UploadFile, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

import io
import base64
import cv2
import time
import numpy as np
import pytesseract

app = FastAPI()

# app.mount("/static", StaticFiles(directory="src/static"), name="static")
templates = Jinja2Templates(directory="templates")


def get_result(image_file):
    start_time = time.time()
    image_bytes = image_file.file.read()
    decoded_img = cv2.imdecode(np.frombuffer(image_bytes, np.uint8), -1)
    text = pytesseract.image_to_string(decoded_img)
    encoded_string = base64.b64encode(image_bytes)
    bs64 = encoded_string.decode('utf-8')
    image_data = f'data:image/jpeg;base64,{bs64}'
    e_time = "--- %.5f seconds ---" % (time.time() - start_time)
    return {
        "text": text,
        "inference_time": e_time,
        "message": "success",
        "status": status.HTTP_200_OK,
        "image_data": image_data
    }


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/")
async def home_predict(request: Request, file: UploadFile = File(...)):
    result = None
    error = None
    try:
        result = get_result(image_file=file)

    except Exception as ex:
        error = ex
    return templates.TemplateResponse("index.html", {"request": request, "result": result, "error": error})


@app.get("/api")
def read_root():
    return {
        "message": "Welcome to the API",
        "status": status.HTTP_200_OK
    }


@app.post("/ocr")
async def compute_ocr(request: Request, file: UploadFile = File(...)):
    try:
        return get_result(image_file=file)
    except Exception as e:
        return {"status": status.HTTP_400_BAD_REQUEST, "error": e.__str__(), }
