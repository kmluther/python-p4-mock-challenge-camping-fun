from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

db = SQLAlchemy()

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'Name: {self.name} | Difficulty: {self.difficulty}'
    
    serialize_rules = ('-created_at', '-updated_at', '-signups', '-campers')

    signups = db.relationship('Signup', backref='activity')
    campers = association_proxy('signups', 'camper')

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'Time: {self.time} | Camper_ID: {self.camper_id} | Activity_ID: {self.activity_id}'
    
    serialize_rules = ('-created_at', '-updated_at', '-camper_id', '-activity_id')

    @validates('time')
    def validate_time(self, key, time):
        if not 0 <= time <= 23:
            raise ValueError('Time must be between 0 and 23')
        return time

class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default = db.func.now())
    updated_at = db.Column(db.DateTime, onupdate = db.func.now())

    def __repr__(self):
        return f'Name: {self.name} | Age: {self.age}'
    
    serialize_rules = ('-created_at', '-updated_at', '-signups', '-activities')

    signups = db.relationship('Signup', backref='camper')
    activities = association_proxy('signups', 'activity')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('Camper must have name')
        return name
    @validates('age')
    def validate_age(self, key, age):
        if 8 < age > 18:
            raise ValueError('Age must be between 8 and 18')
        return age



# add any models you may need. 