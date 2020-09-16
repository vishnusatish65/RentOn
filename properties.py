from flask import Blueprint
from flask import request
import jwt
import json
from read_function import read
from write_function import write
import time

properties = Blueprint("properties", __name__)


# api for getting list of properties avaliable
@properties.route('/listings', methods=['POST', 'GET'])
def listings():
    try:
        auth_token = request.json['auth_token']

        key = "secret"
        data = jwt.decode(auth_token, key)
        if data['expire'] >= time.time():
            listings = read("property")
            list_listing = []
            for listing in listings:
                if listing["status"] == "a":
                    listing["id"] = int(listing["id"])
                    listing["area"] = int(listing["area"])
                    listing["number_of_bedrooms"] = int(listing["number_of_bedrooms"])
                    listing["amenities"] = list(listing["amenities"].split(","))
                    list_listing.append(listing)
            respone = {"header":auth_token, "body":list_listing}
            return respone
        else:
            return {"message": "Login Time Out"}
    except KeyError:
        return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}


# api to add/delete/modify details of a particular house
@properties.route('/modify/<prop_id>', methods=['POST'])
def modify_properties(prop_id):
    try:
        auth_token = request.json['auth_token']
        key = "secret"
        data = jwt.decode(auth_token, key)
        # check if the person is an owner or admin
        property_data = read("property")
        for row in property_data:
            if row["id"] == prop_id:
                if row["owner_id"] == data["user_id"]:
                    if data['expire'] >= time.time():
                        property_details = {}
                        property_details["id"] = prop_id
                        property_details["area"] = request.json["area"]
                        property_details["number_of_bedrooms"] = request.json["number_of_bedrooms"]
                        property_details["amenities"] = request.json["amenities"]
                        property_details["furnishing"] = request.json["furnishing"]
                        property_details["locality"] = request.json["locality"]
                        property_details["owner_id"] = data['user_id']
                        property_details["status"] = "a"

                        write(property_details, "property", "a")

                        return {"status":"true","message": "property added"}
                              
                    else:
                        return {"status":"false","message":"Timeout"}
                else:
                    return {"status":"False","message": "unauthorised"}
    except KeyError:
        return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}


@properties.route('/modify/<prop_id>', methods=['DELETE'])
def delete_property(prop_id):
    try:
        auth_token = request.json['auth_token']
        key = "secret"
        data = jwt.decode(auth_token, key)
        # check if the person is an owner or admin
        property_data = read("property")
        for row in property_data:
            if row["id"] == prop_id:
                if row["owner_id"] == data["user_id"]:
                    if data['expire'] >= time.time():
                            listings = read("property")
                            list_listing = []
                            for listing in listings:
                                if listing['id'] == id:
                                    if listing['owner_id'] != data['user_id']:
                                        return {"status":"false","message": "Not the Owner"}
                                else:
                                    list_listing.append(listing)

                            write(list_listing, "property", "w")

                            return {"status":"true","message": "property deleted"}
    except KeyError:
        return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}


@properties.route('/modify/<prop_id>', methods=['PATCH'])
def update_property(prop_id):
    try:
        auth_token = request.json['auth_token']
        key = "secret"
        data = jwt.decode(auth_token, key)
        print(data)
        # check if the person is an owner or admin
        property_data = read("property")
        for row in property_data:
            if row["id"] == prop_id:
                if row["owner_id"] == data["user_id"]:
                    property_details = {}
                    property_details["id"] = prop_id
                    property_details["area"] = request.json["area"]
                    property_details["number_of_bedrooms"] = request.json["number_of_bedrooms"]
                    property_details["amenities"] = request.json["amenities"]
                    property_details["furnishing"] = request.json["furnishing"]
                    property_details["locality"] = request.json["locality"]
                    property_details["owner_id"] = data['user_id']
                    property_details["status"] = "a"
                    listings = read("property")
                    list_listing = []
                    for listing in listings:
                        if listing['id'] == prop_id:
                                list_listing.append(property_details)
                        else:
                            list_listing.append(listing)

                    write(list_listing, "property", "w")
                    return{"status":"true","message": "property updated"}
                else:
                    return {"status":"false","message": "Not the Owner"}
    # except KeyError:
    #     return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}                   

                    