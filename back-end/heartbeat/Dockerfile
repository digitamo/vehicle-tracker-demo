FROM python:3.7

COPY . /heartbeat
WORKDIR /heartbeat

RUN apt-get update && apt-get install -y curl
RUN apt-get update && apt-get install -y gcc python3-dev musl-dev libpq-dev

RUN pip install --trusted-host pypi.python.org -r requirements.txt

WORKDIR /

CMD ["gunicorn", "-b", "0.0.0.0:4000", "heartbeat.app:application"]