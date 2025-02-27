FROM python:latest

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --upgrade pip

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY ./app /backend/app
COPY ./scripts /backend/scripts

COPY entrypoint.sh /backend/

#COPY ./certificates /backend/certificates

#COPY /.env /backend/app

WORKDIR /backend/app

#CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
#CMD ["uvicorn", "main:app", "--ssl-keyfile", "../certificates/privkey.pem", "--ssl-certfile", "../certificates/fullchain.pem", "--host", "0.0.0.0", "--port", "80", "--reload"]
