
#FROM nginx:1.25.5-alpine
#COPY . /usr/shared/nginx/html 
FROM python:3.9-slim

COPY . . 

RUN pip install -r requirements.txt

CMD gunicorn --bind 0.0.0.0:5000 app:app



