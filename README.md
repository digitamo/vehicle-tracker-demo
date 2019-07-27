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