from datetime import datetime, timedelta


from .db import db


class Purchase(db.Model):
    __tablename__ = "purchases"

    # Properties
    id = db.Column(
        db.Integer,
        primary_key=True)
    vendor_product_id = db.Column(
        db.Integer,
        db.ForeignKey('vendor_products.id'),
        nullable=False)
    sender_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    recipient_user_id = db.Column(
        db.Integer,
        db.ForeignKey('users.id'),
        nullable=False)
    declined = db.Column(
        db.Boolean,
        nullable=False,
        default=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now() + timedelta(days=30))
    expires_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now())
    completed_at = db.Column(
        db.DateTime,
        nullable=True,
        default=None)

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
