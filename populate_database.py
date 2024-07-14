# scripts/populate_database.py
from api.models import db, Resource
from app import create_app

def populate_resources():
	app = create_app()
	with app.app_context():
		resources = [
			{"name": "CS Learning Centre", "description": "Lot 17 Izotsha Rd, Marburg", "city": "Port Shepstone"},
			{"name": "Inkosi Albert Luthuli Central Hospital", "description": "800 Vusi Mzimela Road, Cato Manor", "city": "Durban"},
			{"name": "KZN Children's Hospital", "description": "10 Prince Street, South Beach", "city": "Durban"},
			{"name": "Greys Hospital", "description": "Townbush Road, Athlone", "city": "Pietermaritzburg"},
			{"name": "Townhill Hospital Child and Adolescent Unit", "description": "1 Hyslop Road", "city": "Pietermaritzburg"},
			{"name": "Edenvale Hospital", "description": "CNR Dr Naidoo Drive and Viola Road, Sydenham", "city": "Durban"},
			{"name": "Frere Hospital", "description": "Amalinda Main Rd, Braelyn", "city": "East London"},
			{"name": "Cecilia Makiwane Hospital", "description": "4 Billie Rd, Mdantsane Unit 4", "city": "East London"},
			{"name": "Frontier Hospital", "description": "1 Kingsway Road", "city": "Queenstown"},
			{"name": "Grey Hospital", "description": "54 Kings Rd", "city": "King William’s Town"},
			{"name": "Nelson Mandela Academic Hospital", "description": "Sisson St, Fort Gale", "city": "Mthatha"},
			{"name": "Edenvale Hospital", "description": " ", "city": "Johannesburg"},
			{"name": "South Rand Hospital", "description": " ", "city": "Johannesburg"},
			{"name": "Rahima Moosa Coronationville Mother and Child Hospital", "description": " ", "city": "Johannesburg"},
			{"name": "Chris Hani Baragwanath Academic Hospital", "description": " ", "city": "Johannesburg"},
			{"name": "Charlotte Maxeke Johannesburg Academic Hospital", "description": " ", "city": "Johannesburg"},

		]
		for resource_data in resources:
			resource = Resource(name=resource_data['name'], description=resource_data['description'], city=resource_data['city'])
		db.session.add(resource)
		db.session.commit()

if __name__ == "__main__":
    populate_resources()
    print("Resources added to the database successfully!")
