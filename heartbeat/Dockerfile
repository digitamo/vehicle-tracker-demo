FROM python:3.6-alpine
# NOTE: Consider using a base image and a final image.

COPY . /heartbeat
WORKDIR /heartbeat

RUN apk update && apk add curl
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

WORKDIR /

CMD ["gunicorn", "-b", "0.0.0.0:4000", "heartbeat.app:application"]