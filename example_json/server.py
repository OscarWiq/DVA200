# Detta är ett proof of concept varför den andra versionen med SQLAlchemy är bättre

from flask import Flask, jsonify, request, abort, make_response, url_for
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

param_id = "id"
param_header = "header"
param_body = "body"
param_time = "time"
param_user = "username"
param_result = "result"

@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password) 
    return False

@auth.error_handler
def unauthorized():
    return make_response(jsonify({param_result: "403, Unauthorized access"}), 403)

@app.errorhandler(400)
def not_found():
    return make_response(jsonify({param_result: "400, Bad request"}), 400)

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({param_result: "404, Not found"}), 404)

with open ("usrs.json", "r") as u:
    usrs = json.load(u)
users = usrs
print(str(users))

@app.route("/login", methods=["GET"])
@app.route("/login/", methods=["GET"])
@auth.login_required
def index():
    return jsonify({param_result: [True, "Hello, %s!" % auth.username()]})

if __name__ == "__main__":
    app.run(debug=True, ssl_context='adhoc')
