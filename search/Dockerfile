FROM python:3.6

COPY . /src
WORKDIR /src

RUN apt-get update && apt-get install -y curl

RUN pip install --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80

CMD ["gunicorn", "-b", "0.0.0.0:4000", "app:application"]