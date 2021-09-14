from flask import Blueprint, Flask, request, make_response, jsonify
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash
from project import db
import jwt
import datetime 
from functools import wraps
from project.models import Patient, Appointment, Doctor
from flask_cors import CORS
patient_api_bp = Blueprint('patient_api_bp', __name__)
CORS(patient_api_bp)

def patient_token_required(f):
    @wraps(f)
    def patient_decorated(*args, **kwargs):
        token = None
        if request.args.get('token'):
            token = request.args.get('token')
        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401
        try: 
            data = jwt.decode(token, current_app.config['SECRET_KEY'])
            current_patient = Patient.query.filter_by(id=data['id']).first()
        except:
            return jsonify({'message' : 'Token is invalid!'}), 401
        return f(current_patient, *args, **kwargs)
    return patient_decorated


@patient_api_bp.route('/login', methods=['POST'])
def patient_login():
    data = request.get_json()
    if not data and not data['username'] and not data['password']:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})
    patient = Patient.query.filter_by(username=data['username']).first()
    if not patient:
        return make_response('Could not verify', 401, {'WWW-Authenticate':'Login required'})

    if check_password_hash(patient.password, data['password']):
        token = jwt.encode({'id' : patient.id, 'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=600)}, current_app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')}) 
    
    return jsonify({'message': 'Invaild email or password'})   


@patient_api_bp.route('/register', methods=['POST'])
def create_user():
    data = request.get_json()
    email_exist = Patient.check_email_exist(data['email'])
    if email_exist:
        return jsonify({'message':'There is already an account with this email id!'}, 201)
    username_exist = Patient.check_username_exist(data['username'])
    if username_exist:
        return jsonify({'message':'There is already an account with this username!'}, 201)
    hashed_password = generate_password_hash(data['password'], method='sha256')
    new_patient = Patient(name=data['name'], email=data['email'], username=data['username'], password=hashed_password)
    db.session.add(new_patient)
    db.session.commit()
    return jsonify({'message':'New Patient created'}, 200)


@patient_api_bp.route('/make_appointment', methods=['POST'])
@patient_token_required
def make_appointment(current_patient):
    if not current_patient:
        return jsonify({'message' : 'Invaild Authorization Request!'})

    data = request.get_json()
    patient_id = current_patient.id

    date = data['appointment_date']
    time = data['appointment_time']
    doctor_id = data['doctor_id']

    doctor = Doctor.query.filter_by(id=doctor_id).first()
    if not doctor:
        return jsonify({"message":"Doctor doesn't exist"})
    datetime_str = date + ' ' + time
    appointment_date_time = ""
    try:
        appointment_date_time = datetime.datetime.strptime(datetime_str,'%d-%m-%Y %I:%M%p')
    except:
        return jsonify({'message':'Invalid date or time format'})    

    new_appointment = Appointment(doctor_id=doctor.id, patient_id=patient_id, appointment_date_time=appointment_date_time)
    db.session.add(new_appointment)
    db.session.commit()
    return jsonify({'message':'New appointment created'})




