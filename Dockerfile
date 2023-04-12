FROM python:3.9-alpine

WORKDIR /code

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["sh", "-c", "celery -A project worker -l info"]
