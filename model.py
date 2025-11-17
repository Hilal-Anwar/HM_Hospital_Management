from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    type: Mapped[str]


class Department(db.Model):
    __tablename__ = "departments"
    department_id = db.Column(db.Integer, primary_key=True)
    department_name = db.Column(db.String)
    department_description = db.Column(db.String)
    doctor_list = db.Column(db.JSON)


class Doctor(db.Model):
    __tablename__ = "doctor"
    doctor_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    doctor_name = db.Column(db.String)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    experience = db.Column(db.Integer)
    status = db.Column(db.String)


class Patient(db.Model):
    __tablename__ = "patient"
    patient_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    patient_name = db.Column(db.String)
    status = db.Column(db.String)


class Appointment(db.Model):
    __tablename__ = "appointments"
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    status = db.Column(db.String)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.String)


class Treatment(db.Model):
    __tablename__ = "treatments"
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'))
    diagnosis = db.Column(db.String)
    prescription = db.Column(db.String)
    notes = db.Column(db.String)

class DoctorsUnavailability(db.Model):
    __tablename__ = "doctors _unavailability"
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    date = db.Column(db.Date)
    eight_twelve = db.Column(db.JSON)
    four_nine = db.Column(db.JSON)

class Medicine(db.Model):
    __tablename__ = "medicines"
    medicine_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String)