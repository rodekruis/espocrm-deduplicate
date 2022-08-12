FROM python:3.9-slim-bullseye

ADD credentials /credentials

WORKDIR /pipeline
ADD pipeline .
RUN pip install .
