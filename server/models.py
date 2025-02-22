from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy import ForeignKey, CheckConstraint

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)
    _password_hash = db.Column(db.String)
 
    recipes = db.relationship('Recipe', back_populates='user')
    
    serialize_rules = ('-recipes.user', )
    
    @hybrid_property
    def password_hash(self):
        raise AttributeError
    
    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')
    
    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))
    
    def __repr__(self):
        return f'id: {self.id}, \
            username: {self.username}, \
            image: {self.image_url}, \
            bio: {self.bio}'

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    __table_args__ = (CheckConstraint('LENGTH(instructions) >= 50'),)
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)
    
    user_id = db.Column(db.Integer, ForeignKey('users.id'))
    user = db.relationship('User', back_populates='recipes')