
## Solution architectural sketch

![Alt text](misc/vehicle tracker architecture.jpg?raw=true "architectural sketch")

## Solution design:

### Back end:

 On an architectural level The solution makes use of event sourcing to keep track of the heartbeat events and CQRS for 
 separating write and read operations. This enables the system have an accurate log of the heartbeat -ping messages- 
 from the vehicles. More over it would introduce sympathy between the system and the domain which is inherently event-based.
 
#### Stack:
 - Flask as a micro framework for building micro-services.
 - SqlAlchemy as an ORM, with Flask-Migrate for database migrations.
 - unittest python module for writing unit tests and integration tests.
 - nose test module as a test runner. 
 - postgres as a database.
 
 `NOTE: ` I had to use postgres as a database solution due to time constrains. But Ideally I would have used different database
 for storing events (preferably elasticsearch) and a relational database for the association between customers and vehicles.
  
And the whole back end is orchestrated by docker swarm


### Front end:

#### Stack:
- Angular as a framework to build the single page app
- Jasmine and Karma were used to write unit tests and integration tests. 

### Automation test:

- unittest python module for writing the test cases.
- Selenium for writing the test cases logic.

### CI/CD:

For continuous integration / continuous delivery Travis were used for running unit tests and building and pushing docker 
images to docker registry (dockerhub)


## How the solution will make use of cloud:

In the case of the back end the a cloud provider would be providing the infrastructure the app would be running on including 
the virtual machine across multiple regions which would be used as nodes in our clusters, network interfaces for communication between nodes and in 
some cases we would be hosting SSL certificates and managing our DNS.

On the front end side we can use the cloud to provide us with  CDN hosting service to introduce high availability and
faster respond time to users.


## Deployment steps:

Please find instructions on deployment steps below: 
- [back-end](back-end/README.md)
- [front-end](back-end/README.md)
- [automation test](tests/README.md)
- [simulation](misc/simulation/README.md)


## Serverless architecture proposal:

In the case of using the serverless architecture for for the same challenge the cloud provider would take care of orchestrating
the services (functions) wither by templates or a web console. auto scaling would be handled by the cloud provider as well.
To expose the serverless functions to to be invoked we can use an api gateway.

For data storage we can use elasticsearch for storing events and a relational database (possibly postgres) for storing
relational data like customer and vehicles data. We have the option to use self-managed database or use database as a
service.

We would have 2 serverless functions one for writing events (the heartbeat function) and the other for searching/filtering
(the search function)   

![Alt text](misc/serverless.jpg?raw=true "serverless architecture")

