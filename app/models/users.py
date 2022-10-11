from app.db import db
from typing import List
import datetime
from flask import session, request
import jwt
import os
from functools import wraps


class UsersModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    roles = db.Column(db.Text())
    active = db.Column(db.Integer, nullable=False)

    def __init__(self, kwargs):
        for property, value in kwargs.items():
            # depending on whether value is an iterable or not, we must
            # unpack it's value (when **kwargs is request.form, some values
            # will be a 1-element list)
            if hasattr(value, '__iter__') and not isinstance(value, str):
                # the ,= unpack of a singleton fails PEP8 (travis flake8 test)
                value = value[0]

            if property == 'password':
                value = value # we need bytes here (not plain str)

            setattr(self, property, value)

    def __repr__(self):
        return 'UsersModel(username=%s)' % (self.username)

    def json(self):
        return {
                        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3000),
                        "iat": datetime.datetime.utcnow(),
                        "username": self.username,
                        "id": self.id,
                        "roles": self.roles
                    }

    @classmethod
    def find_by_name(cls, username) -> "UsersModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id) -> "UsersModel":
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_all(cls) -> List["UsersModel"]:
        return cls.query.all()

    def save_to_db(self) -> None:
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self) -> None:
        db.session.delete(self)
        db.session.commit()
