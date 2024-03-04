from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = '	postgres://aqkszvwx:OycNjUCe11qSRUqZUIUSt8cMRPI7IPYF@stampy.db.elephantsql.com/aqkszvwx ' 
app.config['JWT_SECRET_KEY'] = 'super-secret'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
  