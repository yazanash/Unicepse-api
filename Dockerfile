FROM python:3.9-slim-buster

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV FLASK_APP=app.py


EXPOSE 5000
CMD ["flask","run","--debug","--host=0.0.0.0"]