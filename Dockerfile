FROM python:3.10.11-slim

RUN pip install --upgrade pip
COPY ./requirements.txt /
RUN pip install -r requirements.txt
COPY . .
WORKDIR /
