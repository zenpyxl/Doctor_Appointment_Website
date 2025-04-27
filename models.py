
# This following code contains these OOPS concepts.
# 1) Encapsulation: Bundling of data with the methods that operate on data.
# 2) Abstraction: hides the complexity of database interactions.
# 3) Inheritance: All models inhert from db.model (base class from SQLAlchemy).
# 4) Polymorphism: uses custom string representation of objects, which is method overriding.
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
class Doctor(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    specialization = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    appointments = db.relationship('Appointment', backref='doctor', lazy=True)

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Patient(db.Model):
    id = db.Column(db.String(10), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    appointments = db.relationship('Appointment', backref='patient', lazy=True)

class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(20), nullable=False)
    doctor_id = db.Column(db.String(10), db.ForeignKey('doctor.id'), nullable=False)
    patient_id = db.Column(db.String(10), db.ForeignKey('patient.id'), nullable=False)

    def __str__(self):
        return f"{self.time} with {self.doctor}"
