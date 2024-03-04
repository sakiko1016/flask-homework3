from flask import request, jsonify, url_for
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from app import app, db
from models import User

@app.route('/register', methods=['POST'])
def register():
    email = request.json['email']
    password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
    
    user = User(email=email, password=password)
    db.session.add(user)
    db.session.commit()

    return jsonify({'msg': 'User created successfully'}), 201

@app.route('/login', methods=['POST'])  
def login():
    email = request.json['email']
    password = request.json['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id)
        return jsonify({'access_token': access_token})

    return jsonify({'msg': 'Invalid email or password'}), 401

@app.route('/profile', methods=['GET'])
@jwt_required()
def profile():
    return jsonify(user_id=current_user.id, email=current_user.email) 

@app.route('/cars', methods=['GET', 'POST'])
@jwt_required()
def cars():
    if request.method == 'GET':
        cars = Car.query.all()
        return jsonify([car.to_dict() for car in cars])
    
    if request.method == 'POST':
        make = request.json['make']
        model = request.json['model']
        year = request.json['year']

        car = Car(make=make, model=model, year=year) 
        db.session.add(car)
        db.session.commit()

        return jsonify(car.to_dict()), 201

@app.route('/cars/<int:id>', methods=['GET', 'PUT', 'DELETE'])  
@jwt_required()
def car(id):
    car = Car.query.get(id)

    if not car:
        return jsonify({'msg': 'Car not found'}), 404
    
    if request.method == 'GET':
        return jsonify(car.to_dict())

    if request.method == 'PUT':
        car.make = request.json['make']
        car.model = request.json['model']
        car.year = request.json['year']
        db.session.commit()
        return jsonify(car.to_dict())

    if request.method == 'DELETE':
        db.session.delete(car)
        db.session.commit()
        return jsonify({'msg': 'Car deleted'})

if __name__ == '__main__':
    app.run()