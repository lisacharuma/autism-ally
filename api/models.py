from .db import db
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
ma = Marshmallow()


user_resource_association = db.Table('user_resource_association',
	db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
	db.Column('resource_id', db.Integer, db.ForeignKey('resource.id'), primary_key=True)
)

# User Model
class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(150), nullable=False, unique=True)
	email = db.Column(db.String(150), nullable=False, unique=True)
	password = db.Column(db.String(150), nullable=False)
	city = db.Column(db.String(80), nullable=False)
	image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
	posts = db.relationship('Post', back_populates='user', lazy='dynamic')
	resource = db.relationship('Resource', secondary=user_resource_association, back_populates='user')

	def __repr__(self):
		return f"User('{self.username}', '{self.email}', '{self.image_file}')"


#Post Model
class Post(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
	content = db.Column(db.Text, nullable=False)
	title = db.Column(db.String(200), nullable=False)

	user = db.relationship('User', back_populates='posts')


#Resource Model
class Resource(db.Model):
	__tablename__ = 'resource'
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(150), nullable=False)
	description = db.Column(db.String(200), nullable=True)
	city = db.Column(db.String(80), nullable=False)
	user = db.relationship('User', secondary=user_resource_association, back_populates='resource')

#SuccessStory Model
class SuccessStory(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(150), nullable=False)
	content = db.Column(db.Text, nullable=False)

# For serialization and deserialization
class UserSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = User

class PostSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Post

class ResourceSchema(ma.SQLAlchemyAutoSchema):
	class Meta:
		model = Resource
