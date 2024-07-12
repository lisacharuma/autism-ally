from flask import Blueprint, request, jsonify
from .models import Resource, db
from api.db import db  # Import Database setup
from sqlalchemy.exc import SQLAlchemyError
from .blueprint import api_views


@api_views.route('/resources', methods=['GET'])
def show_resources():
	try:
		resources = Resource.query.all()
		return jsonify([resource.serialize() for resource in resources])
	except SQLAlchemyError as e:
		return jsonify({'error': str(e)}), 500


@api_views.route('/resources', methods=['POST'])
def create_resource():
	try:
		data = request.get_json()
		name = data.get('name')
		description = data.get('description')
        city = data.get('city')

		new_resource = Resource(name=name, description=description, city=city)
		db.session.add(new_resource)
		db.session.commit()
        
		return jsonify(new_resource.serialize()), 201
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/resources/<int:id>', methods=['PUT'])
def update_resource(id):
	try:
		data = request.get_json()
		resource = Resource.query.get(id)
		if not resource:
			return jsonify({'error': 'Resource not found'}), 404

		resource.name = data.get('name', resource.name)
		resource.description = data.get('description', resource.description)
		resource.city = data.get('city', resource.city)

		db.session.commit()

		return jsonify(resource.serialize())
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500


@api_views.route('/resources/<int:id>', methods=['DELETE'])
def delete_resource(id):
	try:
		resource = Resource.query.get(id)
		if not resource:
			return jsonify({'error': 'Resource not found'}), 404

		db.session.delete(resource)
		db.session.commit()

		return jsonify({'message': 'Resource deleted successfully'})
	except SQLAlchemyError as e:
		db.session.rollback()
		return jsonify({'error': str(e)}), 500
