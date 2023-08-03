FROM python:3.10

WORKDIR /app

COPY . .

RUN pip3 install -r req.txt


#CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000" ]