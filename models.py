class Doctor:
    def __init__(self, name, specialization, id):
        self.name = name
        self.specialization = specialization
        self.id = id
        self.appointments = []

    def __str__(self):
        return f"Dr. {self.name} ({self.specialization})"

class Patient:
    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.my_appointments = []
        self.password = None

class Appointment:
    def __init__(self, doctor, patient, time):
        self.doctor = doctor
        self.patient = patient
        self.time = time

    def __str__(self):
        return f"{self.time} with {self.doctor}"