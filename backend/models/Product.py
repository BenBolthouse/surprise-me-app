from .mixins.Entity import EntityMixin
from .db import db


class Product(db.Model, EntityMixin):
    __tablename__ = "products"

    name = db.Column(
        db.String(128),
        nullable=False)
    description = db.Column(
        db.String(),
        nullable=True)
    price = db.Column(
        db.Float(precision=2),
        nullable=False,
        default=00.00)
    latitude = db.Column(
        db.Float(precision=5),
        nullable=False,
        default=00.00000)
    longitude = db.Column(
        db.Float(precision=5),
        nullable=False,
        default=000.00000)

    def to_dict(self):
        return {
            **self.entity_to_dict(),
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
        }

    def __init__(self, name, description, price, latitude, longitude):
        self.name = name
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
