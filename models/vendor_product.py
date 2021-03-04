from .db import db


class VendorProduct(db.Model):
    __tablename__ = "vendor_products"

    # Properties
    id = db.Column(
        db.Integer,
        primary_key=True)
    vendor_id = db.Column(
        db.Integer,
        db.ForeignKey('vendors.id'),
        nullable=False)
    name = db.Column(
        db.String(64),
        nullable=False)
    price = db.Column(
        db.Float(5, 2),
        nullable=False)

    # Associations
    _vendor = db.relationship(
        "Vendor",
        back_populates="_products")

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
