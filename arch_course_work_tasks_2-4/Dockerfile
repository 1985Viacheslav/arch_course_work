FROM python:3.11

WORKDIR /backend

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONBUFFERED 1

COPY requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir -r /backend/requirements.txt

COPY .env .

COPY . .

EXPOSE 8000
