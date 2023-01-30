# Bhub Challenge: Back end

This project is a simple python application, using the FastAPI framework, that can be used to perform perform basic CRUD
operations on a SQLite relational test database. It also has a user authentication mechanism, with JWT token and hashed user passwords stored within its DB.

## Why these technologis was chosen?

- Fast API is a simple and light framework, but perfect for this kind of app, in which we could still use powerful tools like dependency injection and decorators to simplify the development

- Schema validation with Pydantic to automatically deal with payload structures

- SQLAlchmemy is a great ORM for Python, which works very well with Pydantic and can also generate a simple db file based on SQLite for test requests

## Installation and set up

To run and test this application, user should apply/follow the steps bellow:

- Have Python 3.11+ and pip 22.3+ installed on local machine

- Clone this project/git repo on local machine

- Go to the directory where the repo was cloned and create a Python virtual environment

```bash
python -m venv venv
```

- Then run this virtual environment:

    - On Windows, run:

```bash
venv\Scripts\activate.bat
```

    - On Unix based SO, run:

```bash
source venv/bin/activate
```

- Install the project dependencies inside de virtual environment:

```bash
pip install -r requirements.txt
```

- Still in a virtual env, start the uvicorn server to run the application on localhost:8000 (by default):

```bash
uvicorn app.main:app --reload
```

Now users can use its own browser to access 'http://localhost:8000/docs' to have a nice and friendly Swagger UI view of the application endpoints and make test requests. An alternative it's to use the Postman app to make the requests.

## Usage and testing

Currently, this basic CRUD application has only few endpoints:

- /login (POST)
- /user (GET, POST)
- /clients (GET, POST, PUT, DELETE)
- /bankdata (GET, POST, PUT, DELETE)

The '/login' endpoint needs to be accessed with the 'POST' verb, passing as body parameters, the 'username' and 'password'. If user make a request passing valid credentials, 
they'll receive a response body (in JSON format) with a generated token. With this token, the user can access/make requests on the other endpoints, since they pass "Bearer <token>" 
on the Authorization header value on the other requests. Without this mentioned token, it's not possible to access the other endpoints, the user will receive an 401 
UNAUTHORIZED http response.

Is important to notice that, for development/test purposes, the endpoint POST /user, which creates a user profile, is not protected, so the tester should start from creating a test profile with password using it.

Considering the user has logged (passed the authentication route), they can make a simple GET request at '/data' endpoint and receive a simple message 'Acesso permitido para 
<username>'.

Considering the user has logged (passed the authentication route), it is possible to perform requests to 3 resources: users itself, clients and bank accounts. The way the business logic was structured, each client can have zero or more bank accounts, while the bank account can be held by just one client. Deleting a client, should also delete all of its bank accounts in the system.

## What can be improved

Due to the short deadline and the basic nature of this application, a lot could be improved, either in terms of codebase/business logic complexity and deployment/infrastructure:

- Implementation of unit and integration tests

- Use a separated and more complex Relational DB (for instance, Postgres), also dockerized (ideally DB should be separated)

- Key-value DB for caching, giving a better latency to our general system

- Key-value DB timestamp base, like Prometheus integrated with Grafana, for better visibility

- Reverse proxy integrated with logging and load balancers, for better latency and throughput

- SSL certificates for HTTPS communication

- Dockerize the Fast API application

- Deploy on a Cloud provider

- Optional Firebase authentication integration

- Integration with a Blob Storage (Azure, AWS, ...) to save related PDF or image files from clients and accounts

- Develop gRPC interfaces to communicate this back end application with another Bhub services written in different coding languages

- A complete CRUD for user entity

- Different roles for different users, giving different permissions

- A better validation (with Regex) of the fields, before saving them at the DB

- Pagination of JSON responses when they return a list of objects

- As the project grows in complexity and gets more resources, would be preferable to have more "layers"

    - Separated "business logic layer" to deal with validations, aggregations, calculations etc

    - Separated "DTO (Data Transfer Object) layer" files for each resource/entity we have in the system

    - Separated and customized exception objects


Pull requests are welcome. There's a lot that can improve in this project.
