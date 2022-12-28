# syntax=docker/dockerfile:1

FROM python:3.8-slim-buster

ARG WORKDIR
ENV WORKDIR $WORKDIR
WORKDIR ${WORKDIR}

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . ${WORKDIR}


CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=8080"]
EXPOSE 8080