import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_TRACK_MODIFICATIONS = False
POSTGRES_USER = 'admin'
POSTGRES_PASSWORD = 'password'
POSTGRES_DB = 'dev'
POSTGRES_URL = 'localhost:5432'
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=POSTGRES_USER,
    pw=POSTGRES_PASSWORD,
    url=POSTGRES_URL,
    db=POSTGRES_DB
)
