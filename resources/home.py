from flask_restful import Resource


# noinspection PyUnreachableCode
class Home(Resource):
    def get(self):
        return {'message': 'This is the canib4lvegan0 homepage'}, 200
