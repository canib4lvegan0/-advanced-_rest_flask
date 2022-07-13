from flask_restful import Resource


# noinspection PyUnreachableCode
class Aline(Resource):
    def get(self):
        return {'message': 'Eu te amo, pretinha <3. Beba agua, viu?'}, 200
