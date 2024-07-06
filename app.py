from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from api.db import db        #imports the database setup
from api.models import ma
from flask_cors import CORS  # Import the CORS module
import os
from api.models import User, Resource, SuccessStory, DiscussionPost


# the application factory
def create_app():
    app=Flask(__name__)
    app.secret_key = "AutismAlly"


    """Database configuration"""
    basedir = os.path.abspath(os.path.dirname(__file__))
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')

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

    @app.route('/register', methods=['POST'])
    def register():
        data = request.get_json()
        hashed_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User registered successfully!'})

    @app.route('/login', methods=['POST'])
    def login():
        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()
        if user and check_password_hash(user.password, data['password']):
            session['user_id'] = user.id
            session['username'] = user.username
            return jsonify({'message': 'Login successful!'})
        return jsonify({'message': 'Invalid credentials!'}), 401

    return app
app = create_app()

if __name__ == "__main__":
    # Importing db here ensures it's imported within the application context.
    #from app import db
    # Create the database tables based on the defined models
    #with app.app_context():
     #   db.create_all()
    app.run(debug=True)
