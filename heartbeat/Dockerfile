FROM python:3.7
# NOTE: Consider using a base image and a final image.

COPY . /heartbeat
WORKDIR /heartbeat

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y gcc python3-dev musl-dev libpq-dev

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

WORKDIR /

CMD ["gunicorn", "-b", "0.0.0.0:4000", "heartbeat.app:application"]