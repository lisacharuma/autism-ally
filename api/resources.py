from flask import Blueprint, request, jsonify
from .models import ResourceSchema, Resource, db
from api.db import db  # Import Database setup
from sqlalchemy.exc import SQLAlchemyError
from .blueprint import api_views

# Initializing schema
resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)


@api_views.route('/resources', methods=['GET'])
def show_resources():
	try:
		resources = Resource.query.all()
		return jsonify(resources_schema.dump(resources))
	except SQLAlchemyError as e:
		return jsonify({'error': str(e)}), 500


@api_views.route('/resources', methods=['POST'])
def create_resource():
	try:
		data = request.get_json()
		name = data.get('name')
		address = data.get('address')
		city = data.get('city')

		new_resource = Resource(name=name, address=address, city=city)
		db.session.add(new_resource)
		db.session.commit()
        
		return jsonify(resource_schema.dump(new_resource)), 201
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
		resource.address = data.get('address', resource.address)
		resource.city = data.get('city', resource.city)

		db.session.commit()

		return jsonify(resource_schema.dump(resource))
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
