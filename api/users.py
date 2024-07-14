from flask import redirect, request, jsonify, session, url_for
from api.db import db  # Import Database setup
from flask_bcrypt import Bcrypt
from .models import UserSchema, User
from .blueprint import api_views

bcrypt = Bcrypt()

"""Get all recorded users"""
@api_views.route("/users", methods=["GET"], strict_slashes=False)
def get_users():
	users = User.query.all()
	user_schema = UserSchema(many=True)
	return jsonify(user_schema.dump(users))


"""Get a single user"""
@api_views.route("/users/<int:user_id>", methods=["GET"], strict_slashes=False)
def get_user(user_id):
	user = User.query.get(user_id)
	if user:
		user_schema = UserSchema()
		return jsonify(user_schema.dump(user)), 200
	else:
		return jsonify({"error": "User not found"}), 404


"""Create a new user"""
@api_views.route("/signup", methods=["POST"], strict_slashes=False)
def create_user():
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


"""Login existingUser"""
@api_views.route("/login", methods=["POST"], strict_slashes=False)
def login_user():
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
		session['user_id'] = user.id
		return jsonify(success=True), 200
	return jsonify(success=False, message='Invalid credentials')



"""Update an existing user"""
@api_views.route("/users/<int:user_id>", methods=["PUT"], strict_slashes=False)
def update_user(user_id):
    user = User.query.get(user_id)
    if not user: # user doesn't exist, exit gracefully
        return jsonify({"error": "User not found"}), 404

    data = request.json
    if "username" not in data and "email" not in data:
        return jsonify({"error": "No data provided for update"}), 400

    if "username" in data:
        user.username = data["username"]

    if "email" in data:
        user.email = data["email"]

    db.session.commit()
    user_schema = UserSchema()
    return jsonify(user_schema.dump(user))


"""Delete an existing user"""
@api_views.route("/users/<int:user_id>", methods=["DELETE"], strict_slashes=False)
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user: # user doesn't exist, exit gracefully
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})
