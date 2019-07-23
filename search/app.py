import os

from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

# Read DB URI from environment.

# TODO: Use postgres.
# TODO: Use a postgres db engine good for writing operations. and another one for reading.

# Construct Flask application.
application = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS')
application.config.from_object(app_settings)

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
