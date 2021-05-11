from flask import Blueprint, jsonify, request


product_routes = Blueprint("product_routes", __name__, url_prefix="/api/v1/products")


# GET https://surprise-me.benbolt.house/api/v1/products?lon...&lat...&lev...
# Given a geocoordinate location retrieves a list of all nearby products.
@product_routes.route("")
def get():
    latitude = request.params.get("lat")
    longitude = request.params.get("lon")
    zoom_level = request.params.get("lev")

    raise Exception("Not implemented")
