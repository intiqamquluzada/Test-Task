FROM python:3.9-slim-buster

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install selenium
RUN apt-get update && apt-get install -y chromium-driver

COPY . .

CMD ["sh", "-c", "celery -A project worker -l info"]
