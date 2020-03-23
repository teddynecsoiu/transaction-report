# Transaction API

A simple transaction API that makes use of SQLite database to insert and fetch transaction information.

The project comes with OpenAPI specification which you can find on  public [Swagger UI](https://app.swaggerhub.com/apis-docs/teddynecsoiu/transaction/1.0.0) page or in the `/docs` folder.



## Running the app



#### Running the app locally

Assuming you have `python3` and `pip3` already installed on your system.

```bash
# Set up local virtual enviroment
python3 -m venv env
source env/bin/activate
pip3 install -r requirements.txt

# First inialize the database then run the app
python3 db_init.py
python3 app.py
```

> When running locally, `unix` based systems could generated the database file without group write permissions. If you can't seem to be able to update the database, just run the line below.

```bash
chmod +w transactions.sqlite
```


#### Running the app in a docker container

Best if you are missing dependencies (e.g. SQLite C client) or Python on your machine.

```bash
# Assuming you are in the project folder
# Build and run the Docker image
docker build -t transaction-api .
docker run -d -p 5000:5000 transaction-api
```



## TODO

* Add Docstring documentation
* E2E Tests, DBB, TDD, Unit, etc
* More robust validation
* Pep 8 (nice to have)
* Improve error handling
* Add endpoint to export modified record as CSV
* Move SQL to `schema.sql`
