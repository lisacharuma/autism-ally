from flask_bcrypt import Bcrypt #for paswd hashing
from datetime import datetime
from app import db, create_app
from api.models import User, Post, Comment, Resource
from werkzeug.security import generate_password_hash

bcrypt = Bcrypt()

app = create_app()
app.app_context().push()

# Drop all tables and recreate them
db.drop_all()
db.create_all()

# Sample Users
users = [
    User(username='john_doe', email='john@example.com', password=bcrypt.generate_password_hash('password').decode('utf-8'), city='Durban'),
    User(username='jane_doe', email='jane@example.com', password=bcrypt.generate_password_hash('password').decode('utf-8'), city='Pietermaritzburg'),
    User(username='alice', email='alice@example.com', password=bcrypt.generate_password_hash('password').decode('utf-8'), city='Johannesburg'),
    User(username='bob', email='bob@example.com', password=bcrypt.generate_password_hash('password').decode('utf-8'), city='Durban')
]

# Sample Posts
posts = [
    Post(title='Understanding Autism', content='Autism spectrum disorder (ASD) is a developmental disability caused by differences in the brain.', user_id=1, date_posted=datetime.utcnow()),
    Post(title='Autism and Education', content='Children with autism can learn and succeed in school with the right support.', user_id=2, date_posted=datetime.utcnow()),
    Post(title='Community Support for Autism', content='Join our community to share experiences and get support.', user_id=3, date_posted=datetime.utcnow())
]

# Sample Comments
comments = [
    Comment(content='This is very informative, thank you!', post_id=1, user_id=2, date_posted=datetime.utcnow()),
    Comment(content='I agree, my child has benefited greatly from school programs.', post_id=2, user_id=1, date_posted=datetime.utcnow()),
    Comment(content='Thank you for creating this platform.', post_id=3, user_id=4, date_posted=datetime.utcnow())
]

# Sample Resources
resources = [
	Resource(name='CS Learning Centre', address='Lot 17 Izotsha Rd, Marburg', city='Port Shepstone'),
    Resource(name='Inkosi Albert Luthuli Central Hospital', address='800 Vusi Mzimela Road, Cato Manor', city='Durban'),
    Resource(name='KZN Childrens Hospital', address='10 Prince Street, South Beach', city='Durban'),
    Resource(name='Greys Hospital', address='Townbush Road, Athlone', city='Pietermaritzburg'),
    Resource(name='Townhill Hospital Child and Adolescent Unit', address='1 Hyslop Road', city='Pietermaritzburg'),
    Resource(name='Edenvale Hospital', address='CNR Dr Naidoo Drive and Viola Road, Sydenham', city='Durban'),
    Resource(name='Frere Hospital', address='Amalinda Main Rd, Braelyn', city='East London'),
    Resource(name='Cecilia Makiwane Hospital', address='4 Billie Rd, Mdantsane Unit 4', city='East London'),
    Resource(name='Frontier Hospital', address='1 Kingsway Road', city='Queenstown'),
    Resource(name='Grey Hospital', address='54 Kings Rd', city='King William’s Town'),
    Resource(name='Nelson Mandela Academic Hospital', address='Sisson St, Fort Gale', city='Mthatha'),
    Resource(name='Edenvale Hospital', address='5 Mandela Strt ', city='Johannesburg'),
    Resource(name='South Rand Hospital', address='9 Monterey, Marine Drive', city='Johannesburg'),
    Resource(name='Rahima Moosa Coronationville Mother and Child Hospital', address='Rahima Moosa Coronationville Mother and Child Hospital', city='Johannesburg'),
    Resource(name='Chris Hani Baragwanath Academic Hospital', address='Chris Hani Baragwanath Academic Hospital', city='Johannesburg'),
    Resource(name='Charlotte Maxeke Johannesburg Academic Hospital', address='Charlotte Maxeke Johannesburg Academic Hospital', city='Johannesburg'),
    Resource(name='Autism Center2', address='14 Nelson Mandela Drive ', city='Durban'),
    Resource(name='Autism Center 3', address=' 14 Address 5', city='Durban')
]

# Add sample data to the session
db.session.add_all(users)
db.session.add_all(posts)
db.session.add_all(comments)
db.session.add_all(resources)

# Commit the session to the database
db.session.commit()

print("Sample data added successfully!")
