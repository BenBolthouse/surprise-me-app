from flask import Blueprint, jsonify, request
from sqlalchemy import and_, or_


from models import db, Product


product_routes = Blueprint("product_routes", __name__, url_prefix="/api/v1/products")


# GET https://surprise-me.benbolt.house/api/v1/products?lon...&lat...&lev...
# Given a geocoordinate location retrieves a list of all nearby products.
@product_routes.route("", methods=["GET"])
def get():
    latitude = float(request.args.get("lat"))
    longitude = float(request.args.get("lon"))
    radius = float(request.args.get("rad"))

    lat_upper_bound = latitude + radius
    lat_lower_bound = latitude - radius
    lon_upper_bound = longitude + radius
    lon_lower_bound = longitude - radius

    products = Product.query.filter(
        and_(
            Product.latitude < lat_upper_bound,
            Product.latitude > lat_lower_bound,
            Product.longitude < lon_upper_bound,
            Product.longitude > lon_lower_bound)).all()

    products = [x.to_dict() for x in products]

    return jsonify({
        "message": "Success",
        "data": products,
    })
