from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)
from datetime import timedelta
from flask_cors import CORS, cross_origin
import sys
import os


app = Flask(__name__)
jwt = JWTManager(app)
api = Blueprint('account_api', __name__)
CORS(api)


@api.route('/login', methods=['GET', 'POST'])
@cross_origin()
def create_token():
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if email != "test@test.com" or password != "test":
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=email, fresh=True)
    refresh_token = create_refresh_token(identity=email)
    return jsonify(access_token=access_token, refresh_token=refresh_token)


@api.route("/refresh", methods=['GET', 'POST'])
@jwt_required(refresh=True)
def refresh():
    print("HELLO")
    sys.stdout.flush()
    get_token = request.headers.get('Authorization')
    print("this is the refresh_token", get_token)
    sys.stdout.flush()
    identity = get_jwt_identity()
    print("this is the identity", identity)
    sys.stdout.flush()
    new_token = create_access_token(identity=identity, fresh=False)
    response = jsonify(access_token=new_token)
    print("this is the response", response)
    sys.stdout.flush()
    response.headers.add("Access-Control-Allow-Origin", "*")
    print("this is the response", response)
    sys.stdout.flush()
    return response, 200


@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200
