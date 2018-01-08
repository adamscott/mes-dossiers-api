from flask_restful import Resource


class Cases(Resource):
    def get(self):
        return {
            'hello': 'world'
        }