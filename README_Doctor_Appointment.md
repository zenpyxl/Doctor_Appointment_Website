# 🏥 Doctor Appointment Booking System (Python + Flask)

This is a simple web-based Doctor Appointment Booking system built using **Python (Flask)**, incorporating essential **Object-Oriented Programming (OOP)** and **Data Structures and Algorithms (DSA)** concepts. The project allows both **doctors and patients** to register, log in, and manage appointments through a user-friendly interface styled with Bootstrap 5.

---

## 🚀 Features

- ✅ Doctor and Patient Registration with secure login
- ✅ Auto-generated unique IDs (Doctor: `d001`, Patient: `p0001`, etc.)
- ✅ Patient can book appointments only after logging in
- ✅ Doctors can view and delete booked appointments
- ✅ Session-based authentication for both roles
- ✅ Dynamic slot allocation using DSA concepts
- ✅ Responsive UI using Bootstrap 5

---

## ⚙️ How to Run

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/doctor-appointment-system.git
   cd doctor-appointment-system
   ```

2. **Install Required Packages**
   ```bash
   pip install flask
   ```

3. **Run the App**
   ```bash
   python app.py
   ```

4. **Visit in Browser**
   ```
   http://127.0.0.1:5000
   ```

---

## 🧠 OOP Concepts Used

- ### Encapsulation:  
  Data and methods are bundled inside class structures for `Doctor`, `Patient`, and `Appointment`.

- ### Abstraction:  
  Complex logic for generating IDs and managing appointments is abstracted in class methods.

- ### Object Instantiation:
  ```python
  class Doctor:
      def __init__(self, name, specialization, id):
          self.name = name
          self.specialization = specialization
          self.id = id
          self.password = None
          self.appointments = []

  doctor = Doctor("Sita", "Dermatology", "d002")
  ```

- ### Relationships Between Classes:
  The `Appointment` class holds references to both `Doctor` and `Patient` objects.

---

## 📚 DSA Concepts Used

### ✅ Queue Data Structure – TimeSlotQueue

Appointment slots for each doctor are managed using a **queue**, ensuring **FIFO** (first come, first serve) booking order.

```python
class TimeSlotQueue:
    def __init__(self):
        self.queue = []

    def add_slot(self, slot):
        self.queue.append(slot)

    def get_slot(self):
        return self.queue.pop(0) if self.queue else None
```

- Used to manage available time slots like `["10:00 AM", "11:00 AM", "12:00 PM"]`
- Ensures that patients are given the earliest available slot automatically

---

## 🛠️ Functional Overview

### 👤 Patient Registration
- Automatically assigns a unique patient ID (`p0001`, `p0002`, ...)
- Stores name and password securely in-memory

### 👨‍⚕️ Doctor Registration
- Assigns a unique doctor ID (`d001`, `d002`, ...)
- Stores specialization and password

### 📅 Booking Appointments
- Only logged-in patients can book
- Select a doctor and receive the next available time slot from that doctor's queue

### 🧾 Doctor Dashboard
- Logged-in doctors can view all appointments
- Appointments can be deleted (time slot is not restored in current version)

---

## 🔐 Login Credentials (Sample)
### Preloaded:
- Doctor ID: `d001`, Password: set during registration
- Patient ID: `p0001`, Password: set during registration

Each user must register once to get their login credentials.

---

## 📝 TODO (Improvements)
- Persistent storage with SQLite or MySQL
- Forgot password / email validation
- Role-based admin panel
- Pagination for large appointment lists

---

## 📄 License
MIT License. Free to use and modify.
