FROM python:3.7.8-slim
LABEL maintainer="yunica"



RUN mkdir /code
WORKDIR /code

COPY . .
RUN pip install --no-cache-dir .