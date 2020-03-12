FROM python:3.7-alpine as base

ENV PYTHONUNBUFFERED=0

WORKDIR /app

COPY . .
