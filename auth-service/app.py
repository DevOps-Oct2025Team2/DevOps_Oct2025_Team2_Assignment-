from flask import Flask
from flask_migrate import Migrate
from db import db
import models

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql+psycopg2://auth_user:auth_pass@localhost:5433/auth_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.get("/health")
def health():
    return {"status": "ok"}
