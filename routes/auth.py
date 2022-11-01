#from crypt import methods
#from urllib import request
from flask import Blueprint, jsonify, request
from funcion_jwt import write_token, valida_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data['username'] == "Yonhatan Ramirez" and data['password'] == 12345:
        return write_token(data=request.get_json())
    else:
        response = jsonify({"message": "User not found"})
        response.status_code = 404
        return response
    
@routes_auth.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return valida_token(token, output=True)    


