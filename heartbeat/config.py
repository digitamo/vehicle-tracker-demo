import os

# USER = os.environ.get('DB_USER')
# PASSWORD = os.environ.get('DB_PASSWORD')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig:
    """Production configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI',
    #                                          os.environ.get('DB_URI',
    #                                                         'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')))
    # NOTE: Uncomment this when using postgres.
    # SQLALCHEMY_DATABASE_URI = f'postgres://{USER}:{PASSWORD}@db:5432/users'
    with open(os.environ.get('POSTGRES_USER_FILE'), 'r') as file:
        POSTGRES_USER = file.read()
    with open(os.environ.get('POSTGRES_PASSWORD_FILE'), 'r') as file:
        POSTGRES_PASSWORD = file.read()
    with open(os.environ.get('POSTGRES_DB_FILE'), 'r') as file:
        POSTGRES_DB = file.read()
        
    DB_HOST = 'postgres'
    DB_PORT = '5432'
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://{user}:{passwd}@{host}:{port}/{db}'.format(
        user=POSTGRES_USER,
        passwd=POSTGRES_PASSWORD,
        host=DB_HOST,
        port=DB_PORT,
        db=POSTGRES_DB)
