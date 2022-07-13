from db import db


# noinspection PyUnreachableCode
class TokenBlockList(db.Model):
    __tablename__ = 'blocklist'

    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    create_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, jti, create_at):
        self.jti = jti
        self.create_at = create_at

    @classmethod
    def find_token(cls, jti_token):
        return cls.query.filter_by(jti=jti_token).first_or_404('Token not found')

    @classmethod
    def get_blocklist(cls):
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
            'jti': self.tji,
            'create at': self.create_at
        }
