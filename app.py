from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from api.blueprint import api_views
from api.db import db        #imports the database setup
from api.models import ma
from flask_cors import CORS  # Import the CORS module
import os
from api.models import User, UserSchema, Resource, Post, Comment, user_resource_association
from api.utils import *

# the application factory
def create_app():
	app=Flask(__name__)
	app.secret_key = "AutismAlly"


	"""Database configuration"""
	basedir = os.path.abspath(os.path.dirname(__file__))
	app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'autism_ally.db')

	"""Sqlalchemy track modification"""
	app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

	"""File upload configuration"""
	app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static/profile_pics')
	app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

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

	#Set the path to the images folder relative to the project dir
	project_root = os.path.dirname(os.path.abspath(__file__))
	upload_folder = os.path.join(project_root, 'images')
	app.config['UPLOAD_FOLDER']=upload_folder

	if not os.path.exists(upload_folder):
		os.makedirs(upload_folder)


	@app.route('/')
	def home():
		"""
		app home page
		"""
		return render_template("index.html")

	@app.route('/about')
	def about():
		"""
		about page
		"""
		return render_template("about.html")

	@app.route('/information')
	def information():
		"""
		Information section
		"""
		return render_template("information.html")

	@app.route('/stories')
	def stories():
		"""
		Stories of well known figures with autism
		"""
		return render_template("stories.html")


	#Only renders template. Logic is in api/users.py
	@app.route('/signup', methods=['GET', 'POST'])
	def signup():
		"""
		sign up page
		"""
		return render_template('signup.html', action='Sign Up', url=url_for('api_views.create_user'))


	@app.route('/login', methods=['GET','POST'])
	def login():
		"""
		login page
		"""
		return render_template('login.html', action='Login', url=url_for('api_views.login_user'))


	@app.route('/dashboard')
	def dashboard():
		"""
		renders dashboard page
		"""
		user_id = session.get('user_id')  # Get the user_id from the session
		username = session.get('username')
		email = session.get('email')

		if 'user_id' not in session:
			return redirect(url_for('login'))

		user = User.query.get(user_id)
		if not user:
			return redirect(url_for('login'))

		all_posts = Post.query.order_by(Post.date_posted.desc()).all()
		for post in all_posts:
			post.comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
		
		# Pass user_id to the template
		return render_template("dashboard.html", user=user, posts=all_posts)


	@app.route('/logout')
	def logout():
		"""
		logs out user
		"""
		session.clear()
		return redirect(url_for('home'))


	@app.route('/profile')
	def profile():
		"""
		user profile page
		"""
		if 'user_id' not in session:
			return redirect(url_for('login'))

		# Fetch the logged-in user's data from the database
		user_id = session['user_id']
		user = User.query.get(user_id)

		return render_template('profile.html', user=user)


	@app.route('/create_post', methods=['GET', 'POST'])
	def create_post():
		"""
		creates new post on user dashboard
		"""
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


	@app.route('/my_posts')
	def my_posts():
		"""
		gets logged in user's posts
		"""
		if 'user_id' not in session:
			return redirect(url_for('login'))

		user_id = session['user_id']
		user = User.query.get(user_id)
		user_posts = Post.query.filter_by(user_id = session['user_id']).order_by(Post.date_posted.desc()).all()

		#Order comments in descending order
		for post in user_posts:
			post.comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
		return render_template('my_posts.html', user=user, posts=user_posts)


	@app.route('/my_resources')
	def my_resources():
		"""
		returns autism help centers near user
		"""
		if "user_id" not in session:
			return redirect(url_for('login'))

		user_id = session['user_id']
		user = User.query.get(user_id)

		# Query to find resources in the user's city
		resources = Resource.query.filter_by(city=user.city).all()

		for resource in resources:
			print(f"Resource: {resource.name}, City: {resource.city}")
		return render_template('my_resources.html', resources=resources)


	@app.route('/profile/update', methods=['GET','POST'])
	def update_profile():
		"""
		updates loged in user's profile
		"""
		if "user_id" not in session:
			return redirect(url_for('login'))
		user_id = session['user_id']
		user = User.query.get(user_id)
		if request.method == 'POST':
			return render_template('update_user.html', url=url_for('api_views.update_user', user_id=user_id))
		return render_template('update_user.html', action='Update Profile', url=url_for('api_views.update_user', user_id=user_id))



	return app
app = create_app()

if __name__ == "__main__":
	# Importing db here ensures it's imported within the application context.
	from app import db
	# Create the database tables based on the defined models
	with app.app_context():
		db.create_all()
		app.run(debug=True)
