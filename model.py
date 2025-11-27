from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint
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


class Appointments(db.Model):
    __tablename__ = "appointments"
    appointment_id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.patient_id'))
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'))
    status = db.Column(db.String)
    appointment_date = db.Column(db.Date)
    appointment_time = db.Column(db.String)


class DoctorsUnavailability(db.Model):
    __tablename__ = "doctors_unavailability"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctor.doctor_id'))
    slot1 = db.Column(db.Integer,default=1)
    slot2 = db.Column(db.Integer,default=1)
    __table_args__ = (UniqueConstraint('date', 'doctor_id',
                                       name='uq_doctors_unavailability_date_doctor'),)


class Medicine(db.Model):
    __tablename__ = "medicines"
    medicine_id = db.Column(db.Integer, primary_key=True)
    medicine_name = db.Column(db.String)


class Treatments(db.Model):
    __tablename__ = "treatments"
    treatment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.appointment_id'))
    visit_type = db.Column(db.String)
    test_done = db.Column(db.String)
    diagnosis = db.Column(db.String)
    medicine_dose = db.Column(db.JSON)
    prescription = db.Column(db.String)
