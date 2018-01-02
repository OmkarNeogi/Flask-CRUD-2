from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

from models.item_model import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )
    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item has to belong to a store ID."
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return {'message': 'item already exists'}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'There was an error inserting the item.'}, 500
        return item.json(), 201

    @jwt_required()
    def put(self, name):
        data = self.parser.parse_args()
        item = ItemModel.find_by_name(name)

        if not item:
            item = ItemModel(name, **data)
        else:
            item.price = data['price']
        item.save_to_db()
        return item.json(), 201

    @jwt_required()
    def delete(self, name):
        item = self.find_by_name()
        if item:
            item.delete_from_db()

        return {'message':'item deleted'}


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in ItemModel.get_all_items()]}
