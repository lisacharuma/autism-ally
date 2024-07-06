from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from flask_bcrypt import Bcrypt  # Import bcrypt for pswd hashing
from api.db import db        #imports the database setup
from api.models import ma
from flask_cors import CORS  # Import the CORS module
import os


# the application factory
def create_app():
    app=Flask(__name__)
    app.secret_key = "AutismAlly"
    return app


@app.route('/')
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()
