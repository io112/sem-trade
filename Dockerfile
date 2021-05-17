FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine

ARG COMMIT
#RUN apk --update add bash nano
RUN apk add --update --no-cache g++ gcc libxslt-dev libxml2-dev libxslt-dev python-dev

RUN mkdir app
COPY ./app/ /app/app/
RUN rm -R /app/app/static/*

RUN echo $COMMIT
RUN mkdir /app/app/static/$COMMIT
COPY ./app/static/development/ /app/app/static/$COMMIT

COPY ./app/uwsgi.ini .
ENV STATIC_PATH /app/app/static
COPY ./requirements.txt .
RUN pip install -r requirements.txt