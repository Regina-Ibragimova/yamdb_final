FROM python:3.8.5

WORKDIR /yamdb_final_code

COPY requirements.txt .

# COPY redoc/redoc.yaml files/static/

RUN pip install -r requirements.txt

COPY . .

CMD gunicorn api_yamdb.wsgi:application --bind 0.0.0.0:8000
