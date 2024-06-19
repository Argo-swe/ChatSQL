FROM python:3.10.14

WORKDIR /usr/src/app

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./app /usr/src/app

CMD ["fastapi", "dev", "app.py", "--host", "0.0.0.0"]
