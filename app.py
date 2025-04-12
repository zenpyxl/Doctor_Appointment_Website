from flask import Flask, render_template, request, redirect, session, url_for
from models import Doctor, Patient, Appointment
from dsa_structures import TimeSlotQueue


import random
def generate_patient_id():
    if patients:
        existing_ids = sorted([int(pid[1:]) for pid in patients.keys()])
        next_id = existing_ids[-1] + 1
    else:
        next_id = 1
    return f"p{next_id:04d}"



def generate_doctor_id():
    if doctors:
        existing_ids = sorted([int(did[1:]) for did in doctors.keys()])
        next_id = existing_ids[-1] + 1
    else:
        next_id = 1
    return f"d{next_id:03d}"


app = Flask(__name__)

# Dummy data
doctors = {
    "d1": Doctor("Ramesh", "Cardiology", "d1"),
    "d2": Doctor("Sita", "Dermatology", "d2")
}
patients = {}
appointment_slots = {
    "d1": TimeSlotQueue(),
    "d2": TimeSlotQueue()
}
# Initialize slots
for doc_id in appointment_slots:
    appointment_slots[doc_id].reset_slots(["10:00 AM", "11:00 AM", "12:00 PM"])

@app.route('/')
def index():
    return render_template("index.html", doctors=doctors)


@app.route('/book', methods=["GET", "POST"])
def book():
    if "user" not in session or session.get("role") != "patient":
        return render_template("book.html", msg=None, doctors=doctors)

    if request.method == "POST":
        pid = session["user"]
        doc_id = request.form["doctor_id"]
        patient = patients[pid]
        doctor = doctors[doc_id]

        slot = appointment_slots[doc_id].get_slot()
        if slot:
            appt = Appointment(doctor, patient, slot)
            doctor.appointments.append(appt)
            patient.my_appointments.append(appt)
            msg = f"Appointment booked at {slot} with {doctor}"
        else:
            msg = f"No slots available for {doctor}"

        return render_template("book.html", msg=msg, doctors=doctors)

    return render_template("book.html", msg=None, doctors=doctors)


    return render_template("book.html", doctors=doctors)

@app.route('/view')
def view():
    return render_template("view.html", doctors=doctors)


app.secret_key = "secret123"

@app.route('/login', methods=["GET", "POST"])
def login():
    msg = ""
    if request.method == "POST":
        user_type = request.form["user_type"]
        user_id = request.form["user_id"]
        password = request.form["password"]

        if user_type == "doctor":
            if user_id in doctors and doctors[user_id].password == password:
                session["user"] = user_id
                session["role"] = "doctor"
                return redirect(url_for("doctor_dashboard"))
            else:
                msg = "Invalid Doctor ID or Password."

        elif user_type == "patient":
            if user_id in patients and patients[user_id].password == password:
                session["user"] = user_id
                session["role"] = "patient"
                return redirect(url_for("index"))
            else:
                msg = "Invalid Patient ID or Password."

    return render_template("login.html", msg=msg)

@app.route('/doctor_dashboard')
def doctor_dashboard():
    if "user" in session and session.get("role") == "doctor":
        doc_id = session["user"]
        return render_template("doctor_dashboard.html", doctor=doctors[doc_id])
    return redirect(url_for("login"))

@app.route('/delete_appointment', methods=["POST"])
def delete_appointment():
    doc_id = request.form["doctor_id"]
    time = request.form["time"]
    doctor = doctors[doc_id]
    doctor.appointments = [appt for appt in doctor.appointments if appt.time != time]
    return redirect(url_for("doctor_dashboard"))



@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("index"))



@app.route('/register_patient', methods=["GET", "POST"])
def register_patient():
    msg = ""
    if request.method == "POST":
        pname = request.form["patient_name"]
        password = request.form["patient_password"]
        pid = generate_patient_id()
        if pid in patients:
            msg = "Patient ID already exists. Try logging in."
        else:
            p = Patient(pname, pid)
            p.password = password
            patients[pid] = p
            msg = f"Registration successful. Your Patient ID is {pid}. Please use it to login."
    return render_template("register_patient.html", msg=msg)



@app.route('/register_doctor', methods=["GET", "POST"])
def register_doctor():
    msg = ""
    if request.method == "POST":
        name = request.form["doctor_name"]
        specialization = request.form["specialization"]
        password = request.form["doctor_password"]
        doc_id = generate_doctor_id()

        d = Doctor(name, specialization, doc_id)
        d.password = password
        doctors[doc_id] = d
        appointment_slots[doc_id] = TimeSlotQueue()
        appointment_slots[doc_id].reset_slots(["10:00 AM", "11:00 AM", "12:00 PM"])
        msg = f"Registration successful. Your Doctor ID is {doc_id}. Please use it to login."
    return render_template("register_doctor.html", msg=msg)


if __name__ == '__main__':
    app.run(debug=True)