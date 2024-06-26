FROM python:3.10.14

WORKDIR /usr/src

RUN mkdir -p /opt/chatsql/db
RUN mkdir -p /opt/chatsql/dictionary_schemas

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./entrypoint-backend.sh ./entrypoint-backend.sh
RUN ["chmod", "+x", "./entrypoint-backend.sh"]

WORKDIR /usr/src/app

COPY ./app /usr/src/app

CMD ["fastapi", "dev", "app.py", "--host", "0.0.0.0"]
