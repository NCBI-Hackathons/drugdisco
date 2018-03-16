FROM python:latest

RUN mkdir /DrugDisco
COPY . /DrugDisco
WORKDIR /DrugDisco

RUN apt-get update && apt-get install -y --no-install-recommends apt-utils
RUN apt-get install -y nodejs
RUN apt-get install -y npm
RUN pip install -r requirements.txt

