import os

from eventsourcing.infrastructure.sqlalchemy.manager import SQLAlchemyRecordManager
from flask import Flask, jsonify
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from heartbeat.domain.application import get_application, init_application

# Read DB URI from environment.
basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: Decouple config.
# TODO: Use postgres.
# TODO: Use a postgres db engine good for writing operations. and another one for reading.

uri = os.environ.get('DB_URI', 'sqlite:////' + os.path.join(basedir, 'data.sqlite'))

# Construct Flask application.
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define database connection.
db = SQLAlchemy(application)

from heartbeat.model import EventSource

migrate = Migrate(application, db)


# Construct eventsourcing application.
@application.before_first_request
def init_example_application_with_sqlalchemy():
    init_application(
        entity_record_manager=SQLAlchemyRecordManager(
            record_class=EventSource,
            session=db.session,
        )
    )


# Define Web application.
@application.route("/heartbeat/<int:vehicle_id>", methods=['POST'])
def hello(vehicle_id):
    app = get_application()
    entity_id = app.create_ping(vehicle_id=vehicle_id).id
    return jsonify({'entity_id': entity_id})


@application.route("/heartbeat/ping", methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})


if __name__ == "__main__":
    # Run the application.
    application.run(host='0.0.0.0', port=5000)
