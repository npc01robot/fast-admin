from apps.test.views.item import ItemResource
from flask import Blueprint
from flask_restful import Api

item_api_bp = Blueprint("item_api", __name__)
item_api = Api(item_api_bp)

item_api.add_resource(ItemResource, "/item/<int:item_id>")
