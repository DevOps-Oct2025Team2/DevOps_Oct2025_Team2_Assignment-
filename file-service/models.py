from db import db

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    owner_user_id = db.Column(db.Integer, nullable=False)
    filename = db.Column(db.String(255), nullable=False)