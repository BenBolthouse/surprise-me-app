from .db import db


class UserPaymentMethod(db.Model):
    __tablename__ = "user_payment_methods"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.id'),
                        nullable=False)
    last_four = db.Column(db.Integer, nullable=False)
    expiration = db.Column(db.Integer, nullable=False)
    exp_date = db.Column(db.DateTime, nullable=False)
    card_number = db.Column(db.String(255), nullable=False)

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
