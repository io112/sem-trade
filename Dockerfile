FROM python:3.8-alpine AS compile-image

ARG COMMIT
#RUN apk --update add bash
RUN apk --update add g++ gcc libxslt-dev libxml2-dev libxslt-dev python3-dev

RUN mkdir app
COPY ./app/ /app/app/
RUN rm -R /app/app/static/*

#RUN echo $COMMIT
RUN mkdir /app/app/static/$COMMIT
COPY ./app/static/development/ /app/app/static/$COMMIT

COPY ./app/uwsgi.ini .
COPY ./requirements.txt .
RUN pip install --user -r requirements.txt

FROM tiangolo/uwsgi-nginx-flask:python3.8-alpine AS build-image
ENV STATIC_PATH /app/app/static
COPY --from=compile-image /root/.cache /root/.cache
COPY --from=compile-image /root/.local /root/.local
COPY --from=compile-image /app/ /app/
COPY  --from=compile-image /app/app/uwsgi.ini /app/uwsgi.ini

