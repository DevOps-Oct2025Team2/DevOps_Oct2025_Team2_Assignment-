# DevOps_Oct2025_Team2_Assignment-
Local Setup (Docker DB + Flask Services) — Team Guide
0) What we’re building locally

We run everything locally using:

Docker Compose to start PostgreSQL databases

Flask services (e.g., auth-service, file-service)

Migrations (Option B) to create tables from version-controlled schema instructions

You will have your own local DB data, I will have my own. We share schema via Git (migrations), not the data itself.

1) What is docker-compose.yml and why do we need it?

docker-compose.yml is a configuration file that tells Docker:

“Start these containers with these settings.”

In our project, it starts two PostgreSQL databases:

auth-db (for auth-service)

file-db (for file-service)

Why this is good

No one needs to install PostgreSQL manually

Everyone runs the same DB version

Easy for markers/QA to run the project

Volumes (IMPORTANT: why you won’t lose data)

Inside docker-compose.yml, we use volumes like this:

volumes:
  auth_db_data:
  file_db_data:


And each DB container maps its data folder to a volume:

volumes:
  - auth_db_data:/var/lib/postgresql/data


What this means:

Your database data is stored in a Docker-managed “storage box” (volume)

If you restart containers (docker compose down then up) your data stays

You only lose DB data if you deliberately delete volumes:

✅ Data persists:

docker compose down
docker compose up -d


❌ Data resets (ONLY if you do this):

docker compose down -v

How you use docker-compose.yml (commands)

Run these at repo root:

Start DB containers (background):

docker compose up -d


Check what is running:

docker ps


Stop containers (data remains because volume stays):

docker compose down

2) “your-service” setup (repeat for auth-service / file-service)

Each service is responsible for:

Its own Flask app

Its own DB connection

Its own models (tables)

Its own migrations folder

So you’ll do steps inside your service folder.

2.1 Enter your service folder

Example for you (auth-service):

cd auth-service

3) Python dependencies (what to install and why)

Install these in your service folder:

python -m pip install flask flask-sqlalchemy flask-migrate psycopg2-binary

What each package is for

flask → the web server / API routes

flask-sqlalchemy → lets us define tables using Python classes

flask-migrate → adds the flask db ... commands (migration system)

psycopg2-binary → allows Python to connect to PostgreSQL

4) What files you need in each service (and what they do)
✅ db.py — database “engine” setup

Purpose: Creates the db object that the whole service uses.

Minimal db.py:

from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

✅ models.py — define your tables here (YOU create your own)

Purpose: This is where you define your database tables (schema) using classes.

Example models.py (just an example — you will create your own tables):

from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")


Important:

You are responsible for your own schema (auth tables)

I am responsible for my own schema (file tables)

We share migrations via Git so both of us can recreate the schema locally

✅ app.py — Flask app + DB connection + migration wiring

Purpose:

Create the Flask app

Connect to your Postgres DB container

Enable migrations (flask db ...)

Minimal migration-ready app.py template:

from flask import Flask
from flask_migrate import Migrate
from db import db
import models  # IMPORTANT: ensures Flask "sees" your table definitions

app = Flask(__name__)

# Change this DB URL depending on service:
# auth-service connects to auth-db (port 5433)
# file-service connects to file-db (port 5434)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql+psycopg2://YOUR_USER:YOUR_PASS@localhost:YOUR_PORT/YOUR_DB"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.get("/health")
def health():
    return {"status": "ok"}

For auth-service DB URL (example)
"postgresql+psycopg2://auth_user:auth_pass@localhost:5433/auth_db"

For file-service DB URL (example)
"postgresql+psycopg2://file_user:file_pass@localhost:5434/file_db"

5) Migrations (Option B) — how tables are created

We do not manually create tables in Postgres.
Instead we use migrations (schema instructions).

5.1 Tell Flask what app to use (Windows PowerShell)

Inside your service folder:

$env:FLASK_APP="app:app"


This means:

app = app.py

app = the Flask variable inside it

5.2 Initialize migrations (first time only)
flask db init


Purpose: creates a migrations/ folder automatically.

What’s inside migrations/

configuration files for the migration tool

a versions/ folder where migration scripts are stored

migration scripts are what we commit to Git

6) What you do as the auth-service developer (summary)

docker compose up -d (repo root) — start DBs

cd auth-service

install dependencies

create db.py, models.py, app.py (with auth-db URL)

$env:FLASK_APP="app:app"

flask db init

Next steps after init (we do later):

flask db migrate -m "..." → generate migration script

flask db upgrade → apply migration to create tables

commit migrations/ folder to Git

fter flask db init (Create tables using migrations)
Preconditions (must be true)

✅ Docker DB containers are running (from repo root):

docker compose up -d
docker ps


You should see your DB container (e.g., file-db or auth-db) Up.

✅ You are in your service folder:

cd your-service


✅ You already ran:

flask db init


and a migrations/ folder exists.

Step 1 — Make sure Flask can “see” your tables
Action

Check your app.py contains this line:

import models

Purpose

If Flask doesn’t import models.py, migration autogeneration will say “No changes detected” because it can’t see your table definitions.

Step 2 — Generate a migration file (create schema instructions)
Action (PowerShell, inside service folder)

Set FLASK_APP:

$env:FLASK_APP="app:app"


Then generate migration:

flask db migrate -m "create initial tables"

Purpose

Creates a migration script (instructions) in:

your-service/migrations/versions/<id>_create_initial_tables.py

Expected output (example)

You should see something like:

Detected added table 'users' or Detected added table 'files'

Generating .../versions/<id>_....py ... done

Step 3 — Apply the migration (actually creates tables in Postgres)
Action
flask db upgrade

Purpose

Runs the migration script against Postgres to create tables.

Expected output

You should see:

Running upgrade -> <id>, create initial tables

Step 4 — Verify tables exist (proof in the DB)
Option A: Verify using psql inside the DB container
For file-service DB
docker exec -it file-db psql -U file_user -d file_db -c "\dt"

For auth-service DB
docker exec -it auth-db psql -U auth_user -d auth_db -c "\dt"

Purpose

Lists tables. You should see:

your app table (e.g., files or users)

alembic_version (migration tracking table)

Step 5 — Commit migration files to Git (so teammate can reproduce schema)
Action (repo root)
git add your-service/migrations
git commit -m "Add initial DB schema for your-service"
git push

Purpose

This shares the schema instructions with the team.
Other devs/QA/CI can apply the same schema by running:

cd your-service
$env:FLASK_APP="app:app"
flask db upgrade

Common issues (fast fixes)
1) “No changes detected”

✅ Fix:

Ensure import models is in app.py

Ensure your model classes exist in models.py
Then rerun:

flask db migrate -m "create initial tables"

2) Password / DB does not exist

✅ Fix:

Make sure docker compose up -d is running

Confirm compose env vars are correct (no typos like PSTGRES_DB)

If DB name was wrong earlier, reset the correct volume once:

docker compose down
docker volume rm <service_volume_name>
docker compose up -d

One-line summary (what you just did)

✅ migrate generates instructions
✅ upgrade executes those instructions to create tables
✅ Commit migrations/ so everyone can recreate the same schema locally

Key rule for teamwork

You create and commit auth-service migrations

I create and commit file-service migrations

We pull and run flask db upgrade to apply each other’s schema locally

We do not share data, only schema

## Sample Users
How Sample Users Are Added

Run these lines in terminal:(you can create more user also)
$env:ADMIN_USERNAME="admin"
$env:ADMIN_PASSWORD="admin123"
$env:USER_USERNAME="user1"
$env:USER_PASSWORD="user123"
python sample_users.py
** You don't need to run this all the time only if when you create new user **


The script will:
Hash passwords using werkzeug.security.generate_password_hash
Insert users into the users table
Skip creation if the user already exists (safe to re-run)


Current Sample Users (Local Dev)
Role	Username	Password
Admin	admin	admin123
User	user1	user123
Passwords are stored as hashes in the database, not in plaintext.