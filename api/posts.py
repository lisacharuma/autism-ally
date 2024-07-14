from flask import Blueprint, request, jsonify
from api.db import db  # Import Database setup
from sqlalchemy.exc import SQLAlchemyError
from .models import Post, PostSchema
from .blueprint import api_views


"""Initialize schema"""
post_schema = PostSchema()
posts_schema = PostSchema(many=True)


@api_views.route('/posts', methods=['GET'])
def show_posts():
	try:
		posts = Post.query.all()
		return jsonify(posts_schema.dump(posts))
	except SQLAlchemyError as e:
		return jsonify({'error': str(e)}), 500


@api_views.route('/posts', methods=['POST'])
def create_post():
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


@api_views.route('/posts/<int:id>', methods=['PUT'])
def update_post(id):
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
