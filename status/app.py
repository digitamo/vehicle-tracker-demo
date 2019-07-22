import os

from eventsourcing.infrastructure.sqlalchemy.manager import SQLAlchemyRecordManager
from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from status.domain.application import get_application, init_application

# Read DB URI from environment.
basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: Decouple config.
# TODO: use postgres.
uri = os.environ.get('DB_URI', 'sqlite:////' + os.path.join(basedir, 'data.sqlite'))

# Construct Flask application.
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define database connection.
db = SQLAlchemy(application)

from .models import IntegerSequencedItem

migrate = Migrate(application, db)


# Construct eventsourcing application.
@application.before_first_request
def init_example_application_with_sqlalchemy():
    init_application(
        entity_record_manager=SQLAlchemyRecordManager(
            record_class=IntegerSequencedItem,
            session=db.session,
        )
    )


# migrate = Migrate(application, db)


# Define Web application.
@application.route("/")
def hello():
    app = get_application()
    entity_id = app.create_new_example(foo='Hello There!').id
    entity = app.example_repository[entity_id]
    return "<h1 style='color:blue'>{}</h1>".format(entity.foo)


if __name__ == "__main__":
    # Run the application.
    application.run(host='0.0.0.0', port=5001)
