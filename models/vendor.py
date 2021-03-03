from .db import db


class Vendor(db.Model):
    __tablename__ = "vendors"

    # Properties
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), nullable=False)
    coord_lat = db.Column(sa.types.DECIMAL(precision=9, scale=6), nullable=False)
    coord_long = db.Column(sa.types.DECIMAL(precision=8, scale=6), nullable=False)

    # Associations
    _products = db.relationship("VendorProduct",
                                back_populates="_vendor",
                                cascade="all, delete-orphan")

    # TODO implement association getters and setters

    # TODO implement scopes while creating routes
