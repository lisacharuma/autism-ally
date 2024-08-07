from flask import redirect, request, jsonify, session, url_for, current_app as app
from flask_login import login_user
from api.db import db  # Import Database setup
from flask_bcrypt import Bcrypt #for paswd hashing
from werkzeug.utils import secure_filename  # validates filenames before saving them to the filesystem
import os
from .models import UserSchema, User
from .blueprint import api_views
from .utils import allowed_file  # Import the allowed_file function

bcrypt = Bcrypt()

@api_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
	"""
	returns all recorded users
	"""
	users = User.query.all()
	user_schema = UserSchema(many=True)
	return jsonify(user_schema.dump(users))


@api_views.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
	"""
	Get a single user
	"""
	user = User.query.get(user_id)
	if user:
		user_schema = UserSchema()
		return jsonify(user_schema.dump(user)), 200
	else:
		return jsonify({"error": "User not found"}), 404


@api_views.route("/signup", methods=["POST"], strict_slashes=False)
def create_user():
	"""
	creates a new user
	"""
	data = request.json
	if 'username' not in data or 'email' not in data:
		return jsonify({"error": "Missing username or email"}), 400

	username = data['username']
	email = data['email']
	password = data['password']
	city = data['city']

	"""Check if email already exist in the database"""
	user = User.query.filter_by(email=email).first() or User.query.filter_by(username=username).first()
	if user:
		return jsonify({"error": "Email already exist, Login instead"})

	user_password = bcrypt.generate_password_hash(password).decode('utf-8')
	new_user = User(username=username, email=email, password=user_password, city=city)
	db.session.add(new_user)
	db.session.commit()

	session['user_id'] = new_user.id
	#user_schema = UserSchema()
	return jsonify({'success': True, 'user_id': new_user.id}), 201


@api_views.route("/login", methods=["POST"], strict_slashes=False)
def user_login():
	"""
	login existing user
	"""
	data = request.json
	print(data)

	if "username" not in data or "password" not in data:
		return jsonify({"error": "Missing username or password"}), 400

	username = data["username"]
	password = data["password"]
	"""Fetch user by username from database"""
	user = User.query.filter_by(username=username).first()
	if user and bcrypt.check_password_hash(user.password, password):
		#user_schema = UserSchema()
		#session['user_id'] = user.id
		login_user(user)
		return jsonify(success=True), 200
	return jsonify(success=False, message='Invalid credentials')


@api_views.route("/users/<int:user_id>", methods=["POST", "PUT"], strict_slashes=False)
def update_user(user_id):
	"""
	updates an existing user
	"""
	user = User.query.get(user_id)
	if not user: # user doesn't exist, exit gracefully
		return jsonify({"error": "User not found"}), 404

	data = request.form
	if not data:
		return jsonify({"error": "No data provided for update"}), 400

	if 'username' in data:
		user.username = data['username']

	if 'email' in data:
		user.email = data['email']

	if 'city' in data:
		user.city = data['city']

	#temporarily removing this
	#if 'image_file' in request.files:
	#	file = request.files['image_file']
	#	if file and allowed_file(file.filename):
	#		filename = secure_filename(file.filename)
	#		file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
	#		try:
	#			file.save(file_path)
	#			user.image_file = filename
	#		except Exception as e:
	#			return jsonify({"error":  f"failed to save file: {str(e)}"}), 500

	db.session.commit()
	user_schema = UserSchema()
	return jsonify(user_schema.dump(user))


@api_views.route("/users/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
	"""
	deletes a user 
	"""
	user = User.query.get(user_id)
	if not user: # user doesn't exist, exit gracefully
		return jsonify({"error": "User not found"}), 404
	db.session.delete(user)
	db.session.commit()
	return jsonify({"message": "User deleted successfully"})
