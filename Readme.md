## Flask Api for Kuantaz 🐍

Flask api to apply for python backend developer at Kuantaz. 
I tried to implement a clean architecture with inversion of 
dependencies and single responsible entities. 
The development was driven by the TDD pattern.

Among the main aspects of the test was the design of 
database models and the handling of information to 
meet the needs of different views. For this reason 
the major developments were found in the persistence 
layer (with [sqlalchemy](https://sqlalchemy.org)) and in the presentation layer 
(with [marshmallow](https://marshmallow.readthedocs.io/en/stable/)). The application layer was limited to 
interacting with the database and the domain layer was omitted. 

## Test Requirements 🧐

- ✅✅ Develop the Rest Api with Flask https://flask.palletsprojects.com/en/2.2.x/
- ✅✅ Use Postgresql database.
- ✅✅ You must create a CRUD for Institutions
  - GET: `/institution`
  - GET: `/institution/{id}`
  - POST: `/institution`
  - PUT: `/institution/{id}`
  - DELETE: `/institution/{id}`
- ✅✅ Create services to list institutions, projects and users.
  - institutions: `/institution`
  - projects: `/project`
  - users: `/user`
- ✅✅ Create service to list an institution (filter by id) with its respective projects and project manager.
  - GET: `/institution/{id}`
- ✅✅ Create a service to list a user (filter by Rut) with their respective projects.
  - GET: `/user?rut=value`
- ✅✅ Create a service to list institutions where to each institution is added to the address the location of google maps example: "https://www.google.com/maps/search/+ direccion" and the abbreviation of the name (only the first three characters).
  - GET: `/institutions/direction` 
- ✅✅ Create service to list projects where the response is the name of the project and the days remaining to completion. 
  - GET: `/projects/durations` 

- ✅✅ Create documentation with Swagger.
  - `/apidocs`
- ✅✅ Use ORM preferably sqlalchemy.
- ✅✅ Unit tests


## Run Project 🥵

The best way to run the project is to execute the following line. 
That will execute the necessary actions to run the docker 
containers to run the tests and then to raise the api and the db.

```bash
$> make run_full_stack
```

To simulate the effect of the above command, the following sequence can be executed 

```bash
$> make run_test_docker
$> make run_api_docker
```

Another option is to run the project using python tools. 
For that you first need to install the dependencies and create the databases. 

- Install the dependencies:
  ```bash
  $> pip install -r requirements.txt
  ```

- Create the database. The api depends on the existence of the 
  databases specified in the environment. By default a database named 
  flask is needed for the api and another one named flask-test is 
  needed for the tests. To create both you can use the commands 
  
  ```bash
  $> make build_db_test
  // run test
  $> make build_db
  // run api 
  ```
  In case you do not want to use docker modify the values of the 
  environment to fit the local settings. 
  An example of the format that the `.env` should have is the [.docker.env](https://github.com/danielorlando97/api-for-kuantaz/blob/main/.docker.env) file

Once you have installed the dependencies and configured 
the necessary databases you can use the following 
commands to run the tests or start the api

```bash
$> make run_test
$> make run_api
```

