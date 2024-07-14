from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from api.blueprint import api_views
from api.db import db        #imports the database setup
from api.models import ma
from flask_cors import CORS  # Import the CORS module
import os
from api.models import User, Resource, SuccessStory, Post, user_resource_association


# the application factory
def create_app():
	app=Flask(__name__)
	app.secret_key = "AutismAlly"


	"""Database configuration"""
	basedir = os.path.abspath(os.path.dirname(__file__))
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'autism_ally.db')

	"""Sqlalchemy track modification"""
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	"""Initialize db"""
	db.init_app(app)
	"""Initialize marshmallow"""
	ma.init_app(app)
	"""Register blueprint"""
	app.register_blueprint(api_views)
	"""implement cors to all origin"""
	cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
	"""Initialize bcrypt"""
	bcrypt = Bcrypt(app)


	@app.route('/')
	def home():
		return render_template("index.html")


	#Only renders template. Logic is in api/users.py
	@app.route('/signup', methods=['GET', 'POST'])
	def signup():
		return render_template('signup.html', action='Sign Up', url=url_for('api_views.create_user'))


	@app.route('/login', methods=['GET','POST'])
	def login():
		return render_template('login.html', action='Login', url=url_for('api_views.login_user'))


	@app.route('/dashboard')
	def dashboard():
		user_id = session.get('user_id')  # Get the user_id from the session
		username = session.get('username')
		email = session.get('email')

		if 'user_id' not in session:
			return redirect(url_for('login'))

		user = User.query.get(user_id)
		all_posts = Post.query.all()
		if not user:
			return redirect(url_for('login'))

		# Pass user_id to the template
		return render_template("dashboard.html", user=user, posts=all_posts)


	@app.route('/logout')
	def logout():
		session.clear()
		return redirect(url_for('home'))

	@app.route('/create_post', methods=['GET', 'POST'])
	def create_post():
		if 'user_id' not in session:
			return redirect(url_for('login'))
		if request.method == 'POST':
			title = request.form['title']
			content = request.form['content']
			new_post = Post(title=title, content=content, user_id=session['user_id'])
			db.session.add(new_post)
			db.session.commit()
			return redirect(url_for('dashboard'))
		return render_template('create_post.html')


	@app.route('/posts')
	def posts():
		all_posts = Post.query.all()
		return render_template('dashboard.html', posts=all_posts)


	@app.route('/my_posts')
	def my_posts():
		if 'user_id' not in session:
			return redirect(url_for('login'))
		user_posts = Post.query.filter_by(user_id=session['user_id']).all()
		return render_template('my_posts.html', posts=user_posts)


	@app.route('/my_resources')
	def my_resources():
		if "user_id" not in session:
			return redirect(url_for('login'))

		user_id = session['user_id']
		user = User.query.get(user_id)

		# Query to find resources in the user's city
		resources = Resource.query.filter_by(city=user.city).all()
		return render_template('my_resources.html', resources=resources)


	@app.route('/update_profile', methods=['POST'])
	def update_profile():
		if 'user_id' not in session:
			return redirect(url_for('login'))
		user = User.query.get(session['user_id'])
		user.username = request.form['username']
		user.email = request.form['email']
		if 'profile_picture' in request.files:
			profile_picture = request.files['profile_picture']
			if profile_picture.filename != '':
				filepath = os.path.join('static/uploads', profile_picture.filename)
				profile_picture.save(filepath)
				user.profile_picture = filepath
		db.session.commit()
		return redirect(url_for('dashboard'))





	return app
app = create_app()

if __name__ == "__main__":
	# Importing db here ensures it's imported within the application context.
	from app import db
	# Create the database tables based on the defined models
	with app.app_context():
		db.create_all()
		app.run(debug=True)
