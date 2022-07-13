from db import db


# noinspection PyUnreachableCode
class StoreModel(db.Model):
    __tablename__ = 'stores'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))

    items = db.relationship('ItemModel', lazy='dynamic')

    def __init__(self, title):
        self.title = title

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first_or_404('Store not found')

    @classmethod
    def get_stores(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'items': [i.to_json() for i in self.items]
        }
