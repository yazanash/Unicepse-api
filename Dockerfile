FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    build-essential \
    libssl-dev \
    libffi-dev \
    python3-dev

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py


EXPOSE 5000
CMD ["flask","run","--host=0.0.0.0"]