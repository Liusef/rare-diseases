# Hi :)

Our project for Hacklytics 2024! Wooo!

### How to install everything

1. run `pip -r requirements.txt` in a python environment.
2. run `npm ci` within the frontend folder.
3. create docker db instance (below)
4. run `python upload_to_database.py in backend` to populate database
5. execute flask through `python app.py` in backend **NOT** `flask run`
6. run `npm run dev` in frontend folder.

### how to use Docker psql

Install Docker Desktop

In root directory, run `docker compose up -d`

This should build the container and automatically run it with your env settings.

### What to put in /.env file:

POSTGRES_DB= whatever you want

POSTGRES_USER= whatever you want

POSTGRES_PASSWORD= whatever you want

POSTGRES_PORT= 5432

HOST_NAME= localhost unless you know what you are doing

HOST_PORT= 5432 unless you know what you are doing

### What to put in /rare_diseases_frontend/.env file:

VITE_APP_PROXY_HOST= IP address to Flask App
