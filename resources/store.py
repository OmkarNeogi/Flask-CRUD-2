from flask_restful import Resource
from models.store_model import StoreModel

class Store(Resource):
	def get(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			return store.json(), 200
		return {'message': 'There are no stores in the database.'}, 404

	def post(self, name):
		if StoreModel.find_by_name(name):
			return {'message': 'A store with name '+str(name)+' already exists.'}

		store = StoreModel(name)
		try:
			store.save_to_db()
		except:
			return {'message': 'The store could not be saved'}, 500
		return {'store': store.json()}, 201

	def delete(self, name):
		store = StoreModel.find_by_name(name)
		if store:
			store.delete_from_db()
			return {'message': 'Store deleted'}
		return {'message': 'store not found'}

class StoreList(Resource):
	def get(self):
		return {'store':[store.json() for store in StoreModel.get_all_items()]}