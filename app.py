from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from api.db import db        #imports the database setup
from api.models import ma
from flask_cors import CORS  # Import the CORS module
import os
from api.models import User, Resource, SuccessStory, Post


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
   # app.register_blueprint(app_views)
    """implement cors to all origin"""
    cors = CORS(app, resources={r"/api/*": {"origins": "*"}})
    """Initialize bcrypt"""
    bcrypt = Bcrypt(app)


    @app.route('/')
    def home():
        return render_template("index.html")

    @app.route('/signup', methods=['GET', 'POST'])
    def signup():
        if request.method == 'POST':
            #Get user data from request
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')  #Hash password
            
            # if username/email already exists render login page
            if User.query.filter_by(username=username).first() or User.query.filter_by(email=email).first():
                return redirect(url_for('login'))  # error='User already exists. Please log in.')

            #Create new user and redirect to their dashboard
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            # Store user's ID in session
            session['user_id'] = new_user.id

            return redirect(url_for('dashboard'))
        return render_template('auth.html', action='Sign Up', url=url_for('signup'))


    @app.route('/login', methods=['GET','POST'])
    def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            #Notify and redirect to login if username/email are not provided
            if not username or not password:
                 return render_template("auth.html", error='Missing username/email or password')
            #Query for the user    
            user = User.query.filter_by(username=username).first()
            if user and bcrypt.check_password_hash(user.password, password):
                session['user_id'] = user.id
                session['username'] = user.username
               # session['email'] = user.email
                return redirect(url_for('dashboard'))
            return 'Invalid credentials'
        return render_template('auth.html', action='Login', url=url_for('login'))


    @app.route('/dashboard')
    def dashboard():
        user_id = session.get('user_id')  # Get the user_id from the session
        username = session.get('username')
        email = session.get('email')

        if 'user_id' not in session:
            return redirect(url_for('login'))

        user = User.query.get(user_id)
        if not user:
            return redirect(url_for('login'))

        # Pass user_id to the template
        return render_template("dashboard.html", user=user)


    @app.route('/logout')
    def logout():
        session.clear()
        return redirect(url_for('home'))

    @app.route('/create_post', methods=['POST'])
    def create_post():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        title = request.form['title']
        content = request.form['content']
        new_post = Post(title=title, content=content, user_id=session['user_id'])
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for('dashboard'))


    @app.route('/posts')
    def posts():
        all_posts = Post.query.all()
        return render_template('posts.html', posts=all_posts)


    @app.route('/my_posts')
    def my_posts():
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user_posts = Post.query.filter_by(user_id=session['user_id']).all()
        return render_template('my_posts.html', posts=user_posts)


    @app.route('/my_resources')
    def my_resources():
        # Implement logic to fetch resources near the user
        user_resources = []  # Replace with actual resources
        return render_template('my_resources.html', resources=user_resources)


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
