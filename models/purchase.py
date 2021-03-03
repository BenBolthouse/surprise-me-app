from .db import db


class Purchase(db.Model):
    __tablename__ = "purchases"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    # TODO implement foreign key property for VendorOffer
    sender_user_id = db.Column(db.Integer,
                               db.ForeignKey('users.id'),
                               nullable=False)
    recipient_user_id = db.Column(db.Integer,
                                  db.ForeignKey('users.id'),
                                  nullable=False)
    declined = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    # TODO set expiration date to 30 days in the future
    expires_at = db.Column(db.DateTime, nullable=False, server_default=db.func.now())
    completed_at = db.Column(db.DateTime, nullable=True, default=None)

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
