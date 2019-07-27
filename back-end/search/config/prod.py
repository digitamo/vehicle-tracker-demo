import os

base_dir = os.path.abspath(os.path.dirname(__file__))
with open(os.environ.get('POSTGRES_USER_FILE'), 'r') as file:
    postgres_user = file.read().strip()
with open(os.environ.get('POSTGRES_PASSWORD_FILE'), 'r') as file:
    postgres_password = file.read().strip()
with open(os.environ.get('POSTGRES_DB_FILE'), 'r') as file:
    postgres_db = file.read().strip()
postgres_url = 'postgres:5432'

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
    user=postgres_user,
    pw=postgres_password,
    url=postgres_url,
    db=postgres_db
)
