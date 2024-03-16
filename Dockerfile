FROM tiangolo/uwsgi-nginx-flask:python3.9

COPY requirements.txt /

WORKDIR /

RUN pip install -r ./requirements.txt --no-cache-dir

COPY /app /app

COPY .env /app/.env
WORKDIR /app

ENV FLASK_APP=app.py
# CMD flask db init && flask db migrate -m "build migration" && flask db upgrade && python -m flask run --host=0.0.0.0 --port=5000
CMD flask db migrate -m "build migration" && flask db upgrade && python -m flask run --host=0.0.0.0 --port=5000