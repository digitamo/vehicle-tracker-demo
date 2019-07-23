import os

# USER = os.environ.get('DB_USER')
# PASSWORD = os.environ.get('DB_PASSWORD')
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class ProductionConfig:
    """Production configuration"""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URI',
                                             os.environ.get('DB_URI',
                                                            'sqlite:////' + os.path.join(BASE_DIR, 'data.sqlite')))
    # NOTE: Uncomment this when using postgres.
    # SQLALCHEMY_DATABASE_URI = f'postgres://{USER}:{PASSWORD}@db:5432/users'
