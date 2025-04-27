# Import framworks
from flask import Flask, render_template, request, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy
from models import db, Doctor, Patient, Appointment
import random

# Intializations Flask app with secret key
with open("secret.key", "r") as f:
    secret_key = f.read().strip()

app = Flask(__name__)
app.secret_key = secret_key


# Connects to a MySQL database named doctor_appointment
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/doctor_appointment'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Displays the homepage
@app.route('/')
def index():
    doctors = Doctor.query.all()
    return render_template("index.html", doctors={doc.id: doc for doc in doctors})

# Booking appointment (Patients)
@app.route('/book', methods=["GET", "POST"])
def book():
    doctors = Doctor.query.all()
    doctor_dict = {doc.id: doc for doc in doctors}

    if "user" not in session or session.get("role") != "patient":
        return render_template("book.html", msg=None, doctors=doctor_dict)

    msg = None
    if request.method == "POST":
        pid = session["user"]
        doc_id = request.form["doctor_id"]
        slot = request.form["time"]  # Get selected time from form
        patient = Patient.query.get(pid)
        doctor = Doctor.query.get(doc_id)

        # Check if this doctor already has an appointment at the selected time
        existing = Appointment.query.filter_by(doctor_id=doc_id, time=slot).first()
        if existing:
            msg = f"Dr. {doctor.name} already has an appointment at {slot}. Please choose another time."
        else:
            appt = Appointment(doctor_id=doc_id, patient_id=pid, time=slot)
            db.session.add(appt)
            db.session.commit()
            msg = f"Appointment booked at {slot} with Dr. {doctor.name}."

    return render_template("book.html", msg=msg, doctors=doctor_dict)

# Doctor Dashboard
@app.route('/doctor_dashboard')
def doctor_dashboard():
    if "user" in session and session.get("role") == "doctor":
        doc_id = session["user"]
        doctor = Doctor.query.get(doc_id)
        return render_template("doctor_dashboard.html", doctor=doctor)
    return redirect(url_for("login"))

# Login (Doctor/Patient)
@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        user_type = request.form["user_type"]
        user_id = request.form["user_id"]
        password = request.form["password"]

        if user_type == "doctor":
            doctor = Doctor.query.filter_by(id=user_id, password=password).first()
            if doctor:
                session["user"] = doctor.id
                session["role"] = "doctor"
                return redirect(url_for("doctor_dashboard"))
            else:
                msg = "Invalid Doctor ID or Password."
        elif user_type == "patient":
            patient = Patient.query.filter_by(id=user_id, password=password).first()
            if patient:
                session["user"] = patient.id
                session["role"] = "patient"
                return redirect(url_for("index"))
            else:
                msg = "Invalid Patient ID or Password."
    return render_template("login.html", msg=msg)

# Logout (Patient/Doctor/Admin)
@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))

# Patient Registration (Sign-up)
@app.route('/register_patient', methods=["GET", "POST"])
def register_patient():
    msg = ""
    if request.method == "POST":
        pname = request.form["patient_name"]
        password = request.form["patient_password"]
        # Generate next sequential patient ID
        last_patient = Patient.query.order_by(Patient.id.desc()).first()
        if last_patient:
            last_num = int(last_patient.id[1:])
            new_num = last_num + 1
        else:
            new_num = 1
        pid = f"p{new_num:04d}"
        new_patient = Patient(id=pid, name=pname, password=password)
        db.session.add(new_patient)
        db.session.commit()
        msg = f"Registration successful. Your Patient ID is {pid}. Please use it to login."
    return render_template("register_patient.html", msg=msg)

# Doctor Registration (Sign-up)
@app.route('/register_doctor', methods=["GET", "POST"])
def register_doctor():
    msg = ""
    if request.method == "POST":
        name = request.form["doctor_name"]
        specialization = request.form["specialization"]
        password = request.form["doctor_password"]
        # Generate next sequential doctor ID
        last_doctor = Doctor.query.order_by(Doctor.id.desc()).first()
        if last_doctor:
            last_num = int(last_doctor.id[1:])
            new_num = last_num + 1
        else:
            new_num = 1
        doc_id = f"d{new_num:03d}"  # Pads with leading zeros (e.g., d001)
        new_doctor = Doctor(id=doc_id, name=name, specialization=specialization, password=password)
        db.session.add(new_doctor)
        db.session.commit()
        msg = f"Registration successful. Your Doctor ID is {doc_id}. Please use it to login."
    return render_template("register_doctor.html", msg=msg)

# My appointments (Doctor)
@app.route('/view')
def view_appointments():
    doctors = Doctor.query.all()
    doctor_dict = {doc.id: doc for doc in doctors}
    return render_template("view.html", doctors=doctor_dict)

# Delete Appointments (Doctor)
@app.route('/delete_appointment/<int:appointment_id>', methods=["POST"])
def delete_appointment(appointment_id):
    if "user" not in session or session.get("role") != "doctor":
        return redirect(url_for("login"))
    
    appt = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for("doctor_dashboard"))

# My appointments (Patient)
@app.route('/my_appointments')
def my_appointments():
    if "user" not in session or session.get("role") != "patient":
        return redirect(url_for("login"))

    pid = session["user"]
    appointments = Appointment.query.filter_by(patient_id=pid).all()

    return render_template("my_appointments.html", appointments=appointments)

# Delete Appointments (Patient)
@app.route('/delete_my_appointment/<int:appointment_id>', methods=["POST"])
def delete_my_appointment(appointment_id):
    if "user" not in session or session.get("role") != "patient":
        return redirect(url_for("login"))

    appt = Appointment.query.get_or_404(appointment_id)

    # Ensure the patient owns this appointment
    if appt.patient_id != session["user"]:
        return "Unauthorized", 403

    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for("my_appointments"))

# Login (Admin)
@app.route('/admin_login', methods=["GET", "POST"])
def admin_login():
    msg = ""
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if username == "admin" and password == "admin123":
            session["user"] = "admin"
            session["role"] = "admin"
            return redirect(url_for("admin_dashboard"))
        else:
            msg = "Invalid credentials."
    return render_template("admin_login.html", msg=msg)

# Admin dashboard (Shows all doctors, patients and appointments)
@app.route('/admin_dashboard')
def admin_dashboard():
    if "user" not in session or session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    doctors = Doctor.query.all()
    patients = Patient.query.all()
    appointments = Appointment.query.all()

    return render_template("admin_dashboard.html",
                           doctors=doctors,
                           patients=patients,
                           appointments=appointments)

# Delete doctor Section (Admin)
@app.route('/admin/delete_doctor/<doctor_id>', methods=["POST"])
def delete_doctor(doctor_id):
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    doctor = Doctor.query.get_or_404(doctor_id)

    # Delete all related appointments first
    Appointment.query.filter_by(doctor_id=doctor_id).delete()

    db.session.delete(doctor)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

# Delete patient section (Admin)
@app.route('/admin/delete_patient/<patient_id>', methods=["POST"])
def delete_patient(patient_id):
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    patient = Patient.query.get_or_404(patient_id)

    # Delete all related appointments first
    Appointment.query.filter_by(patient_id=patient_id).delete()

    db.session.delete(patient)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

# Delete appointment section (Admin)
@app.route('/admin/delete_appointment/<int:appointment_id>', methods=["POST"])
def delete_appointment_admin(appointment_id):
    if session.get("role") != "admin":
        return redirect(url_for("admin_login"))

    appt = Appointment.query.get_or_404(appointment_id)
    db.session.delete(appt)
    db.session.commit()
    return redirect(url_for("admin_dashboard"))

if __name__ == '__main__':
    app.run(debug=True)
