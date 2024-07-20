from flask import Blueprint, request, jsonify, session
from api.db import db  # Import Database setup
from sqlalchemy.exc import SQLAlchemyError
from .models import Post, PostSchema, Comment, CommentSchema, User, UserSchema
from .blueprint import api_views


"""Initialize schema"""
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@api_views.route('/posts', methods=['GET'])
def show_posts():
	"""
	returns all posts
	"""
	try:
		posts = Post.query.all()
		return jsonify(posts_schema.dump(posts))
	except SQLAlchemyError as e:
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts', methods=['POST'])
def create_post():
	"""
	creates a new post
	"""
	try:
		data = request.get_json()
		title = data.get('title')
		content = data.get('content')
		author_id = data.get('author_id')

		new_post = Post(title=title, content=content, author_id=author_id)
		db.session.add(new_post)
		db.session.commit()

		return jsonify(post_schema.dump(new_post)), 201
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts/<int:id>', methods=['GET','PUT'])
def update_post(id):
	"""
	updates an existing post
	"""
	try:
		data = request.get_json()
		post = Post.query.get(id)
		if not post:
			return jsonify({'error': 'Post not found'}), 404

		post.title = data.get('title', post.title)
		post.content = data.get('content', post.content)

		db.session.commit()

		return jsonify(post_schema.dump(post))
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts/<int:id>', methods=['DELETE'])
def delete_post(id):
	"""
	deletes an existing post
	"""
	try:
		post = Post.query.get(id)
		if not post:
			return jsonify({'error': 'Post not found'}), 404

		db.session.delete(post)
		db.session.commit()

		return jsonify({'message': 'Post deleted successfully'})
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts/<int:post_id>/comments', methods=['POST'])
def add_comment(post_id):
	"""
	adds comment to a post
	"""
	data = request.get_json()
	content = data.get('content')

	if not content:
		return jsonify({'error': 'Content is required'}), 400

	post = Post.query.get(post_id)
	if not post:
		return jsonify({'error': 'Post not found'}), 404

	user_id = session.get('user_id')
	if not user_id:
		return jsonify({'error': 'User not logged in'}), 401

	new_comment = Comment(content=content, post_id=post.id, user_id=user_id)

	try:
		db.session.add(new_comment)
		db.session.commit()
		return jsonify({'message': 'Comment added successfully'}), 201
	except Exception as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts/<int:post_id>/comments', methods=['GET'])
def get_comments(post_id):
	"""
	Returns all posts sorted by descending order
	"""
	comments = Comment.query.filter_by(post_id=post_id).order_by(Comment.date_posted.desc()).all()
	return jsonify(comments_schema.dump(comments))
