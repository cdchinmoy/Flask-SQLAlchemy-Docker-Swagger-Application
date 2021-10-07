from flask import Blueprint, Flask, request, make_response, jsonify
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
import jwt
import datetime
from functools import wraps
from project.models import User, Doctor
from flask_cors import CORS

user_api_bp = Blueprint('user_api_bp', __name__)
CORS(user_api_bp)

def user_token_required(f):
    @wraps(f)
    def user_decorated(*args, **kwargs):
        token = None
        if request.args.get('token'):
            token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing!'}, 401)
        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_user = User.query.filter_by(id=data['id']).first()
            print(current_user)
        except:
            return jsonify({'message' : 'Token is invalid!'}, 401)
        return f(current_user, *args, **kwargs)
    return user_decorated             


@user_api_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    email_exist = User.check_email_exist(data['email'])
    if email_exist:
        return jsonify({'message':'There is already an account with this email id!'}, 201)
    username_exist = User.check_username_exist(data['username'])
    if username_exist:
        return jsonify({'message':'There is already an account with this username!'}, 201)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_user = User(name=data['name'], email=data['email'], username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message':'New user created'}, 200)


@user_api_bp.route('/login', methods=['POST'])
def user_login():
    data = request.get_json()
    if not data and not data['username'] and not data['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})
    user = User.query.filter_by(username=data['username']).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})

    if check_password_hash(user.password, data['password']):
        token = jwt.encode({'id' : user.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=600)}, current_app.config['SECRET_KEY'])
        return jsonify({'token' : token.decode('UTF-8')}, 200)
    return jsonify({'message': 'Invaild email or password'}, 201) 


@user_api_bp.route('/create_doctor', methods=['POST'])
@user_token_required
def create_doctor(current_user):
    if not current_user:
        return jsonify({'message' : 'Invaild Authorization Request!'})

    data = request.get_json()
    hashed_password = generate_password_hash(data['password'], method='sha256')
    email_exist = Doctor.check_email_exist(data['email'])
    if email_exist:
        return jsonify({'message':'There is already an account with this email id!'})
    username_exist = Doctor.check_username_exist(data['username'])
    if username_exist:
        return jsonify({'message':'There is already an account with this username!'})
    new_doctor = Doctor(name=data['name'], email=data['email'], username=data['username'], password=hashed_password)
    
    db.session.add(new_doctor)
    db.session.commit()
    return jsonify({'message':'New doctor created'})


@user_api_bp.route('/all_doctor', methods=['GET'])
@user_token_required
def get_all_doctors(current_user):
    if not current_user:
        return jsonify({'message' : 'Invaild Authorization Request!'})

    doctors = Doctor.query.all()
    output = []
    for doctor in doctors:
        doctor_data = {}
        doctor_data['id'] = doctor.id
        doctor_data['name'] = doctor.name
        doctor_data['username'] = doctor.username
        doctor_data['email'] = doctor.email
        doctor_data['password'] = doctor.password
        output.append(doctor_data)

    return jsonify(output,200)       

@user_api_bp.route('/edit_doctor/<id>', methods=['PUT'])
@user_token_required
def edit_doctor(current_user, id):
    if not current_user:
        return jsonify({'message' : 'Invaild Authorization Request!'})

    data = request.get_json()
    try:
        hashed_password = generate_password_hash(data['password'], method='sha256')

        doctor = Doctor.query.get(id)
        doctor.name = data['name']
        doctor.email = data['email']
        doctor.username = data['username']
        doctor.password = hashed_password

        db.session.add(doctor)
        db.session.commit()
        return jsonify({"message":"doctor updated successfully"}, 200)     
    except:
        return jsonify({"message":"No record found"}, 200)  


@user_api_bp.route('/delete_doctor/<id>', methods=['DELETE'])
@user_token_required
def delete_doctor(current_user, id):
    if not current_user:
        return jsonify({'message' : 'Invaild Authorization Request!'})
    try:
        doctor = Doctor.query.get(id)
        db.session.delete(doctor)
        db.session.commit()
        return jsonify({"message":"deleted successfully"}, 200)     
    except:
        return jsonify({"message":"No record found"}, 200)   