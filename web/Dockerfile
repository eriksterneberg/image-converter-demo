FROM python:3.6.5

RUN mkdir -p /home/image_converter/
WORKDIR /home/image_converter/
COPY requirements.txt /home/image_converter/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /home/image_converter/
