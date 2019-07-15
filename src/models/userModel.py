"""'This script intended to handling model for user database"""
from marshmallow import fields, Schema
import datetime
from . import db, bcrypt


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime)
    modified_at = db.Column(db.DateTime)

    # class constructor to set class attributes
    def __init__(self, data):
        self.name = data.get('name')
        self.email = data.get('email')
        self.password = self.__generate_hash(data.get('password'))
        self.created_at = datetime.datetime.utcnow()
        self.modified_at = datetime.datetime.utcnow()

    # method to save users to the db
    def save(self):
        db.session.add(self)
        db.session.commit()

    # method to update user's record on the db
    def update(self, data):
        for key, item in data.items():
            setattr(self, key, item)
            if key == 'password':
                self.password = self.__generate_hash(item)
        self.modified_at = datetime.datetime.utcnow()
        db.session.commit()

    # method to delete record from the db
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    # # method to get all user from db
    # @staticmethod
    # def get_all_users():
    #     return UserModel.query.all()

    # Get single user data:id
    @staticmethod
    def get_one_user(id):
        return UserModel.query.get(id)

    # Get single user data:email
    @staticmethod
    def get_user_by_email(value):
        return UserModel.query.filter_by(email=value).first()

    # Has user's password before saving it to db
    def __generate_hash(self, password):
        return bcrypt.generate_password_hash(password, rounds=10).decode("utf-8")

    # validate user's password during login
    def check_hash(self, password):
        return bcrypt.check_password_hash(self.password, password)

    # return a printable representation of UserModel
    def __repr(self):
        return '<id {}>'.format(self.id)


class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    created_at = fields.DateTime(dump_only=True)
    modified_at = fields.DateTime(dump_only=True)