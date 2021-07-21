from flask import Flask, request, jsonify
from api.routes import api
from flask_jwt_extended import JWTManager
from datetime import timedelta
import os
from database import DB

app = Flask(__name__)
DB.init()
app.config["SECRET_KEY"] = os.getenv('MY_SECRET')
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=30)
app.register_blueprint(api)
app.config['PROPAGATE_EXCEPTIONS'] = True
jwt = JWTManager(app)


@app.route("/")
def index():
    headers = request.headers
    auth = headers.get("X-Api-Key")
    if auth == 'super-secret':
        return jsonify({"message": "OK: Authorized"}), 200
    else:
        return jsonify({"message": "ERROR: Unauthorized"}), 401


if __name__ == "__main__":
    app.run()