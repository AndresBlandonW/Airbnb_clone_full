#!/usr/bin/python3
""" objects that handle all default RestFul API actions for Place - Amenity """
import json
from models.place import Place
from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from os import environ
from flask import abort, jsonify, make_response, request
from flasgger.utils import swag_from


@app_views.route('places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/get_places_amenities.yml',
           methods=['GET'])
def get_place_amenities(place_id):
    """
    Retrieves the list of all Amenity objects of a Place
    """
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)

    amenities = []
    amenity_objects = place.amenities
    for amenity_id in amenity_objects:
        amenities.append(amenity_id.to_dict())
    return jsonify(amenities)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
@swag_from('documentation/place_amenity/delete_place_amenities.yml',
           methods=['DELETE'])
def delete_place_amenity(place_id, amenity_id):
    """
    Deletes a Amenity object of a Place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    place_amenities = place.amenities
    if amenity not in place_amenities:
        abort(404)
    place_amenities.remove(amenity)
    place.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<string:place_id>/amenities/<string:amenity_id>', methods=['POST'],
                 strict_slashes=False)
@swag_from('documentation/place_amenity/post_place_amenities.yml',
           methods=['POST'])
def post_place_amenity(place_id, amenity_id):
    """
    Link a Amenity object to a Place
    """
    place = storage.get("Place", place_id)
    amenity = storage.get("Amenity", amenity_id)
    if place is None or amenity is None:
        abort(404)
    place_amenities = place.amenities
    if amenity in place_amenities:
        print('ya esta')
        return jsonify(amenity.to_dict())
    #place_amenities.append(amenity)
    place_amenities.append(amenity)
    place.save()

    #setattr(place, "amenity_ids", place_amenities)
    return make_response(jsonify(place.to_dict()), 201)
