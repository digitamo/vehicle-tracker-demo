## Running locally

**Dependencies**:

# TODO: include installation links for dependencies.
- docker
- docker-machine
- virtualbox


#### Spin up machine locally:
```
$ docker-machine create --driver virtualbox myvm1
$ docker-machine create --driver virtualbox myvm2
```

#### Setup docker secrets:
```
$ echo "secret_pg_password" | docker secret create pg_password -
$ echo "admin" | docker secret create pg_user -
$ echo "pg_database" | docker secret create pg_database -
```

#### Run docker swarm:
```
$ eval $(docker-machine env myvm1)
$ docker swarm init
```

#### Add nodes to swarm:

```
$ eval $(docker-machine env myvm2)
$ docker swarm join --token <token> <master-node-ip>:2377
```

#### Add redis data folder:
- Create redis data folder in `/home/docker/data` in the master node.

#### Deploy stack:
```
$ docker stack deploy -c docker-compose.yml <stack-name>
```

#### Run DB migrations:
```
$ docker exec -ti <stack-name>_heartbeat.1.$(docker service ps -f 'name=<stack-name>_heartbeat.1' <stack-name>_heartbeat -q --no-trunc | head -n1) /bin/bash
    > cd heartbeat
    > flask db upgrade
```

### Import dummy data.

### Update angular environment.

### Running integration and automation tests.

- Install dependencies
```
$ cd tests
& pip install -r requirements
```

- Install chrome driver for selenium:
    
    If you're running ubuntu you can use this:
    ```
       $ wget https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
       $ unzip chromedriver_linux64.zip
       $ sudo mv chromedriver /usr/bin/chromedriver
       $ sudo chown root:root /usr/bin/chromedriver
       $ sudo chmod +x /usr/bin/chromedriver
    ```
  `NOTE: ` Driver version must match your chrome version.  
    
    if not follow the drivers part of this guide for installing chrome driver [here](https://selenium-python.readthedocs.io/installation.html#downloading-python-bindings-for-selenium). 

