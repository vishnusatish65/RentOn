# all modules imported
from flask import Blueprint
from flask import request
import jwt
import json
from read_function import read
from write_function import write
import time


user = Blueprint("user", __name__)


# new user registeration api
@user.route('/register', methods=['POST'])
def register_user():
    try:
        # getting user details
        new_user_detail = {}
        new_user_detail['id'] = request.json['id']
        new_user_detail['name'] = request.json['name']
        new_user_detail['password'] = request.json['password']
        new_user_detail['email'] = request.json['email']
        new_user_detail['phone_no'] = request.json['phone_no']
        new_user_detail["role"] = request.json['role']

    # calling write function to update the csv file
        write(new_user_detail, "users", "a")
        return{"message": "user registered"}
    except KeyError:
        return{"message": "incomplete details entered"}


# user login
@user.route('/login', methods=['POST'])
def login_user():
    # getting user details
    try:
        username = request.json['name']
        password = request.json['password']
        # reading the csv file and checking  details
        users = read("users")

        flag = False
        role = ""
        for row in users:
            if row['name'] == username:
                if row['password'] == password:
                    flag = True
                    role = row['role']
                    user_id = row['id']
                    break
        # creating JWT token
        if flag:
            payload = {"user_id":user_id, "message": role, "expire": time.time() + 3600}
            key = "secret"
            encode_jwt = jwt.encode(payload, key)
            return {"auth_token": encode_jwt.decode(), "message": "login successful"}
        else:
            return {'message': 'username or password incorrect'}
    except KeyError:
        return{"message": "incomplete details entered"}
    except FileNotFoundError:
        return{"message": "File missing"}


# api for user to rent a house
@user.route('/rent', methods=['POST'])
def rent_house():
    try:
        auth_token = request.json['auth_token']
        house = request.json['id']
        key = "secret"
        data = jwt.decode(auth_token, key)
        # updating listing for the house selected
        if data['expire'] >= time.time():
            listings = read("property")
            list_listing = []
            for listing in listings:
                if listing["id"] == house:
                    if listing['status'] == 'na':
                        return {"message": "house already rented"}
                    else:
                        listing['status'] = 'na'
                        list_listing.append(listing)
                else:
                    list_listing.append(listing)

            write(list_listing, "property", "w")

            return{"message": "House has been rented"}
        else:
            return{"message": "Timed out"}
    except KeyError:
        return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}


# api to get owner detail
@user.route('/details', methods=['POST', 'GET'])
def owner_details():
    try:
        auth_token = request.json['auth_token']
        house = request.json['id']
        key = "secret"
        data = jwt.decode(auth_token, key)

        if data['expire'] >= time.time():
            listings = read("property")
            owner = ""
            for listing in listings:
                if listing["id"] == house:
                    owner = listing["owner"]

            owner_detail = read("users")
            owner_detail_list = {}
            for detail in owner_detail:
                if detail["name"] == owner:
                    owner_detail_list["name"] = detail["name"]
                    owner_detail_list["e-mail"] = detail["email"]
                    owner_detail_list["phone no"] = detail["phone_no"]

            return owner_detail_list
        else:
            return {"message": "Timed out"}
    except KeyError:
        return{"message": "incomplete details entered"}
    except AttributeError:
        return{"message": "data error"}
    except FileNotFoundError:
        return{"message": "File missing"}
