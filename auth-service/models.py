from datetime import datetime
from db import db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)

    role = db.Column(
        db.String(10),
        nullable=False,
        default="user"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

