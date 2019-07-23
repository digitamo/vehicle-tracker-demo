import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Read DB URI from environment.
basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: Decouple config.
# TODO: Use postgres.
# TODO: Use a postgres db engine good for writing operations. and another one for reading.

uri = os.environ.get('DB_URI', 'sqlite://///mnt/workspace/python/tasks/SwedQ/heartbeat/data.sqlite')

# Construct Flask application.
application = Flask(__name__)
application.config['SQLALCHEMY_DATABASE_URI'] = uri
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Define database connection.
db = SQLAlchemy(application)
from search.model import Customer, Vehicle


@application.route("/search", methods=['GET'])
def search():
    customer_name = request.args.get('customer_name')
    reg_no = request.args.get('reg_no')

    vehicles = []

    # TODO: Add pagination.
    if customer_name and reg_no:
        vehicles = Vehicle.query.filter(Vehicle.reg_no.contains(reg_no))
        vehicles = vehicles.join(Customer).filter(Customer.name.contains(customer_name)).all()
    if customer_name:
        vehicles = Vehicle.query.join(Customer).filter(Customer.name.contains(customer_name)).all()
    if reg_no:
        vehicles = Vehicle.query.filter(Vehicle.reg_no.contains(reg_no)).all()

    return jsonify([i.serialize for i in vehicles])


@application.route("/ping", methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})


if __name__ == "__main__":
    # Run the application.
    application.run(host='0.0.0.0', port=5000)
