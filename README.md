# Hi :)


### how to use Docker psql

Install Docker Desktop

In root directory, run `docker compose up -d`

This should build the container and automatically run it with your env settings.

### What to put in root .env file:

POSTGRES_DB= whatever you want

POSTGRES_USER= whatever you want

POSTGRES_PASSWORD= whatever you want

POSTGRES_PORT= 5432

HOST_PORT= 5432 unless you know what you are doing