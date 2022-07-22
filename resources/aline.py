from flask_restful import Resource


# noinspection PyUnreachableCode
class Aline(Resource):

    @classmethod
    def get(cls):
        return {"message": "Beba agua, viu?"}, 200
