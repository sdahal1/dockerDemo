FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /appt_service

WORKDIR /appt_service

ADD . /appt_service/

RUN pip install -r requirements.txt

EXPOSE 8000
