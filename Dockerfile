FROM python:3.8-slim-buster

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY .flaskenv ./
COPY run.py ./
COPY construct.py ./
RUN pip install -r requirements.txt

CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
