from datetime import datetime
from dataholder import db


class User_data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    username = db.Column(db.String(150), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=False)
    address = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False, unique=True)
    phone_no = db.Column(db.String(150), nullable=False, unique=True)
    gender = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(), onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "age": self.age,
            "gender": self.gender,
            "address": self.address,
            "email": self.email,
            "phone_no": self.phone_no,
        }

    def __repr__(self):
        return f"""
        User('{self.id}', '{self.name}', '{self.username}', 
        '{self.age}', '{self.gender}', '{self.address}', 
        '{self.email}', '{self.phone_no}')"""
