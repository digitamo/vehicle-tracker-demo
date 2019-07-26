import datetime
import os

from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

application = Flask(__name__)
CORS(application)

app_settings = os.getenv('APP_SETTINGS')
application.config.from_object(app_settings)

# Define database connection.
db = SQLAlchemy(application)
from search.model import Customer, Vehicle


def filter_by_online(online_str):
    online = True if online_str == 'true' else False
    current_time = datetime.datetime.now()
    minute_ago = current_time - datetime.timedelta(minutes=1)

    if online:
        return Vehicle.query.filter(Vehicle.heartbeat_ts > minute_ago)
    else:
        return Vehicle.query.filter(Vehicle.heartbeat_ts < minute_ago)


@application.route("/search", methods=['GET'])
def search():
    customer_name = request.args.get('customer_name')
    online = request.args.get('online')

    vehicles = []

    # TODO: Add pagination.
    if customer_name is not None and online is not None:
        vehicles = filter_by_online(online)
        vehicles = vehicles.join(Customer).filter(Customer.name.contains(customer_name)).all()
    elif customer_name is not None:
        vehicles = Vehicle.query.join(Customer).filter(Customer.name.contains(customer_name)).all()
    elif online is not None:
        vehicles = filter_by_online(online)
        vehicles = vehicles.all()

    return jsonify([i.serialize for i in vehicles])


@application.route("/search/ping", methods=['GET'])
def ping():
    return jsonify({'message': 'pong'})


if __name__ == "__main__":
    # Run the application.
    application.run(host='0.0.0.0', port=5000)
