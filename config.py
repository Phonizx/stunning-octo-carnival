from flask import Flask, request,jsonify,make_response
from flask_restful import Resource, Api,reqparse
from flask_sqlalchemy import SQLAlchemy


from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    jwt_refresh_token_required, create_refresh_token,
    get_jwt_identity
)
import flask_cors
from flask_cors import CORS,cross_origin
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ["DBURL"]
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #suppressed warnings from sqlalchemy 
app.config['JWT_SECRET_KEY'] = os.environ["JWTSECRET"]


db = SQLAlchemy(app)
jwt = JWTManager(app)
cors = CORS(app)

