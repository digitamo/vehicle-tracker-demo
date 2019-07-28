import os
import random
import logging
import sched, time
import sys

import requests

BASE_URL = os.environ.get('SWARM_IP', 'http://192.168.4.5')
VEHICLE_IDS = [
    'YS2R4X20005399401',
    'VLUR4X20009093588',
    'VLUR4X20009048066',
    'YS2R4X20005388011',
    'YS2R4X20005387949',
    'YS2R4X20005387765',
    'YS2R4X20005387055',
]

scheduler = sched.scheduler(time.time, time.sleep)
logging.basicConfig(stream=sys.stdout, level=logging.INFO)


def simulate_heartbeat(sc):
    online_vehicle_count = random.randrange(7)
    for _ in range(online_vehicle_count):
        vehicle_index = random.randrange(7)
        vehicle_id = VEHICLE_IDS[vehicle_index]
        url = BASE_URL + '/heartbeat/' + vehicle_id

        logging.info('sending a heartbeat for vehicle {vehicle_id}'.format(vehicle_id=vehicle_id))
        response = requests.request("POST", url)
        if response.status_code == 200:
            entity_id = response.json().get('entity_id')
            logging.info('entity id for vehicle {vehicle_id} is {entity_id}'.format(
                vehicle_id=vehicle_id,
                entity_id=entity_id)
            )
        else:
            logging.warning('was not able to send heartbeat message: {message}'.format(message=response.text))

    scheduler.enter(60, 1, simulate_heartbeat, (sc,))


simulate_heartbeat(scheduler)
scheduler.run()
