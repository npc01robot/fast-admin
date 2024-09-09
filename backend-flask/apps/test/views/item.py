from flask_restful import Resource


class ItemResource(Resource):
    def get(self, item_id):
        return {"item_id": item_id}
