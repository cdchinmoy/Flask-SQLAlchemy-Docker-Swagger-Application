from sqlalchemy import create_engine, MetaData, Table, Integer, String, Column, DateTime, ForeignKey, Numeric, SmallInteger
from project import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<User %r>' % self.name

    def check_username_exist(username):
        user = User.query.filter_by(username=username).first()
        if user:
            return user
        else:
            return False

    def check_email_exist(email):
        user = User.query.filter_by(email=email).first()
        if user:
            return user
        else:
            return False        


class Doctor(db.Model):
    __tablename__ = 'doctor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Doctor %r>' % self.name

    def check_username_exist(username):
        doctor = Doctor.query.filter_by(username=username).first()
        if doctor:
            return doctor
        else:
            return False

    def check_email_exist(email):
        doctor = Doctor.query.filter_by(email=email).first()
        if doctor:
            return doctor
        else:
            return False        


class Medicine(db.Model):
    __tablename__ = 'medicine'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(250), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    doctor_id = db.Column(db.Integer, ForeignKey('doctor.id'))

    
class Patient(db.Model):
    __tablename__ = 'patient'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def __init__(self, name, email, username, password):
        self.name = name
        self.email = email
        self.username = username
        self.password = password

    def __repr__(self):
        return '<Patient %r>' % self.name

    def check_username_exist(username):
        patient = Patient.query.filter_by(username=username).first()
        if patient:
            return patient
        else:
            return False

    def check_email_exist(email):
        patient = Patient.query.filter_by(email=email).first()
        if patient:
            return patient
        else:
            return False  

class Appointment(db.Model):
    __tablename__ = 'appointment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.id'))
    appointment_date_time = db.Column(DateTime(), nullable=False)
    created_at = db.Column(DateTime(), default=datetime.now)
    updated_at = db.Column(DateTime(), default=datetime.now, onupdate=datetime.now)
    
    def __init__(self, patient_id, doctor_id, appointment_date_time):
        self.patient_id = patient_id
        self.doctor_id = doctor_id
        self.appointment_date_time = appointment_date_time

    def get_doctor_appointments(doctor_id):
        doctor_appointments = Appointment.query.filter_by(doctor_id=doctor_id)
        if doctor_appointments:
            return doctor_appointments
        else:
            return False

    def get_patient_appointments(patient_id):
        doctor_appointments = Appointment.query.filter_by(patient_id=patient_id)
        if doctor_appointments:
            return doctor_appointments
        else:
            return False        

class Prescription(db.Model):
    __tablename__ = 'prescription'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('patient.id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('appointment.id'))
    medication_id = db.Column(db.Integer, db.ForeignKey('medicine.id'))
    dose = db.Column(db.Integer, nullable=False)
    created_at = db.Column(DateTime(), default=datetime.now)
    updated_at = db.Column(DateTime(), default=datetime.now, onupdate=datetime.now)

    def __init__(self, appointment_id, doctor_id, medication_id, dose):
        self.appointment_id = appointment_id
        self.doctor_id = doctor_id
        self.medication_id = medication_id
        self.dose = dose