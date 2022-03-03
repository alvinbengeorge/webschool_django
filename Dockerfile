FROM python:3.9

RUN mkdir /code
WORKDIR /code

RUN apt-get update && apt-get install -y netcat

COPY requirements.txt /code/
RUN pip install -r requirements.txt

COPY ./ /code/

CMD ./run.sh