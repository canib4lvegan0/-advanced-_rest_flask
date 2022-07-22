from flask_restful import Resource


# noinspection PyUnreachableCode
class Home(Resource):

    @classmethod
    def get(cls):
        return {"message": "This is the canib4lvegan0 homepage"}, 200
