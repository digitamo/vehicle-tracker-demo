FROM python:3.6-alpine
# NOTE: Consider using a base image and a final image.

COPY . /src
WORKDIR /src

RUN apk update && apk add curl
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD ["flask", "db", "upgrade"]

CMD ["gunicorn", "-b", "0.0.0.0:4000", "app:application"]