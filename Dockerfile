# FROM python:3.9-slim
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-slim

RUN apt-get update -y
# RUN apt-get install -y python3-pip python-dev build-essential
# RUN apt update && apt install -y libsm6 libxext6
RUN apt-get -y install tesseract-ocr python3-opencv

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# RUN pip install pillow
# RUN pip install pytesseract
# RUN pip install python-multipart
# RUN pip install opencv-contrib-python jinja2

COPY ./app /app

# EXPOSE 8000
# CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port","${PORT}"]
