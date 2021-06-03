from flask import Flask
from api.routes import api
from flask_jwt_extended import JWTManager

app = Flask(__name__)

app.register_blueprint(api)
app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)

@app.route("/")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()