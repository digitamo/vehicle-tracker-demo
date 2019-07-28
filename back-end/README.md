
## Running locally

**Dependencies**:

- docker
- docker-machine
- virtualbox (required if running locally)


#### 1. Spin up machine:

`NOTE: ` In the case of deployment on the cloud you can use the corresponding driver to your cloud provider. You can 
find docker-machine drivers [here](https://docs.docker.com/machine/drivers/) 

```
$ docker-machine create --driver virtualbox master
$ docker-machine create --driver virtualbox db
$ docker-machine create --driver virtualbox worker1
$ docker-machine create --driver virtualbox worker2
```


#### 2. Enable docker swarm mode:

```
$ eval $(docker-machine env master)
$ docker swarm init
```

If prompted to provide `--advertise-addr` copy the ip address for the `eth1` interface and use

```
$ docker swarm init --advertise-addr <ip-address>
``` 

#### 3. Add nodes to swarm:

After enabling docker swarm mode a command will be printed out with a token to join the cluster copy it or replace the 
parts surrounded by `<>` in the join command with their respective values

```
$ eval $(docker-machine env db)
$ docker swarm join --token <token> <master-node-ip>:2377

$ eval $(docker-machine env worker1)
$ docker swarm join --token <token> <master-node-ip>:2377

$ eval $(docker-machine env worker2)
$ docker swarm join --token <token> <master-node-ip>:2377
```

#### 4. Switch back to the master node:

```
$ eval $(docker-machine env master)
```

#### 5. copy nginx config to the master node:

```
$ docker-machine ssh master "tee -i ./nginx.conf <<< '`cat nginx.conf`'"
```


#### 6. Label the db node:

```
$ docker node update --label-add resource=db db
```


#### 7. Setup docker secrets:

```
$ echo "secret_pg_password" | docker secret create pg_password -
$ echo "admin" | docker secret create pg_user -
$ echo "pg_database" | docker secret create pg_database -
```

#### 8. Deploy the stack:

```
$ docker stack deploy -c docker-compose.yml <stack-name>
```

After deploying the stack you need to wait for the nodes be be running you can monitor the stack in 2 ways
    
   1. Using docker visualizer:
        
        Docker visualizer is included in this compose file and once it's running you can open the url `<master-node-ip>:8080`
   2. Using `docker stack ps`:
   
        `watch docker stack ps <stack-name> -f "desired-state=running"`   
  

#### Run DB migrations:
```
# enable one of the worker nodes
$ eval $(docker-machine env worker1)

# list running containers.
$ docker ps

# copy the container-id of the container with the image 'digitamo/heartbeat'
                |
                ---------
                        |
$ docker exec -it <container-id> bash
    > cd heartbeat
    > flask db upgrade
    > exit
```

### Import dummy data.

You can get the queries for inserting dummy data form the `misc/sql` directory.

```
# enable the db node
$ eval $(docker-machine env db)

# list running containers.
$ docker ps

# copy the container-id of the container with the image 'postgre'
                |
                ---------
                        |
$ docker exec -it <container-id> bash
    > su postgres
    > psql -U admin -d pg_database          
        # paste the insert query from the 'customer.sql` file and press enter
        # paste the insert query from the 'vehicle.sql` file and press enter
    > exit
    > exit

# swith back to the master node
$ eval $(docker-machine env master)
```

At this point the back end should be working and has dummy data up and running across multiple nodes. 


### Clean up.

Run these commands to stop the cluster and clean up.

```
$ eval $(docker-machine env -u)
$ docker-machine rm master
$ docker-machine rm db
$ docker-machine rm worker1
$ docker-machine rm worker2
``` 