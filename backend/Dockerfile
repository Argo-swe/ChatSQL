FROM python:3.10

WORKDIR /usr/src/app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /usr/src/app

CMD ["flask", "run", "--host", "0.0.0.0"]
