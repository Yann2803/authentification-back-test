from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token, create_refresh_token,
    get_jwt_identity
)
from flask_cors import CORS, cross_origin
from database import DB
import sys

app = Flask(__name__)
jwt = JWTManager(app)
api = Blueprint('account_api', __name__)
CORS(api)


@api.route('/login', methods=['GET', 'POST'])
@cross_origin()
def create_token():
    email = request.json.get("email", None)
    print('this is the passwordUpdated', email)
    sys.stdout.flush()
    password = request.json.get("password", None)
    print('this is the passwordUpdated', password)
    sys.stdout.flush()
    if DB.DATABASE.user.find_one({'email': email}) and DB.DATABASE.user.find_one({'password': password}):
        if DB.DATABASE.user.find_one({'email': email})["email"] == email \
                and DB.DATABASE.user.find_one({'password': password})["password"] == password:
            if DB.DATABASE.user.find_one({'email': email})['passwordUpdated']:
                access_token = create_access_token(identity=email, fresh=True)
                refresh_token = create_refresh_token(identity=email)
                return jsonify(access_token=access_token, refresh_token=refresh_token, status=True), 200
            if not DB.DATABASE.user.find_one({'email': email})['passwordUpdated']:
                return jsonify(status=False)
    else:
        return jsonify(confirmation=False), 401


@api.route('/temporary', methods=['GET', 'POST'])
@cross_origin()
def set_password():
    temporary_password = request.json.get("temporaryPassword", None)
    print('this is the isUpdate', temporary_password)
    sys.stdout.flush()
    new_password = request.json.get("newPassword", None)
    print('this is the password', new_password)
    sys.stdout.flush()
    password_updated = request.json.get("passwordUpdated", None)
    print('this is the isUpdate', password_updated)
    sys.stdout.flush()
    if DB.DATABASE.user.find_one({'password': temporary_password}):
        user_id = DB.DATABASE.user.find_one({'password': temporary_password})['_id']
        print('this is the old-password', user_id)
        sys.stdout.flush()
        try:
            DB.DATABASE.user.update_one({"_id": user_id}, {"$set": {'password': new_password}})
            DB.DATABASE.user.update_one({"_id": user_id}, {"$set": {'passwordUpdated': password_updated}})
            return jsonify({"msg": 'password changed'}), 200

        except Exception:
            return jsonify({"msg": "update failed"}), 401
    else:
        return jsonify({"msg": "Bad username or password"}, 401),


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
