from flask import Blueprint, Flask, request, make_response, jsonify
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
import jwt
import datetime
from functools import wraps
from project.models import Doctor, Medicine
from flask_cors import CORS
doctor_api_bp = Blueprint('doctor_api_bp', __name__)
CORS(doctor_api_bp)

def doctor_token_required(f):
    @wraps(f)
    def doctor_decorated(*args, **kwargs):
        token = None
        if request.args.get('token'):
            token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_doctor = Doctor.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_doctor, *args, **kwargs)
    return doctor_decorated


@doctor_api_bp.route('/login', methods=['POST'])
def doctor_login():
    data = request.get_json()
    if not data and not data['username'] and not data['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})
    doctor = Doctor.query.filter_by(username=data['username']).first()
    if not doctor:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})

    if check_password_hash(doctor.password, data['password']):
        token = jwt.encode({'id' : doctor.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=600)}, current_app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')}) 
    
    return jsonify({'message': 'Invaild email or password'})   


@doctor_api_bp.route('/add_medicine', methods=['POST'])
@doctor_token_required
def add_medicine(current_doctor):
    if not current_doctor:
        return jsonify({'message' : 'Invaild Authorization Request!'})

    doctor_id = current_doctor.id
    data = request.get_json()
    new_medicine = Medicine(title=data['title'], price=data['price'], doctor_id=doctor_id)
    db.session.add(new_medicine)
    db.session.commit()
    return jsonify({'message':'New medicine created'})


#### GET ALL APPOINTMENTS ####

