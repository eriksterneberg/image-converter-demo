FROM python:3.7.0-alpine3.8

RUN mkdir -p /home/image_converter/
WORKDIR /home/image_converter/
COPY requirements.txt /home/image_converter/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/image_converter/
