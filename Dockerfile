FROM python:3.9-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt
RUN pip install selenium
RUN apk add chromium-chromedriver

COPY . .

CMD ["sh", "-c", "celery -A project worker -l info"]
