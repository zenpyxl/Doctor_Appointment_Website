
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
   pip install flask flask_sqlalchemy
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

- **Encapsulation**  
  Classes `Doctor`, `Patient`, and `Appointment` encapsulate attributes such as `id`, `name`, `specialization`, `password`, and `time` within the class structure to ensure secure data management.

- **Abstraction**  
  Complexity of raw SQL queries is hidden by using ORM queries with SQLAlchemy, such as fetching doctor or patient records without writing manual SQL commands. Example:  
  ```python
  Doctor.query.filter_by(id=doc_id).first()
  Patient.query.filter_by(id=pid).first()
  ```

- **Inheritance**  
  Classes `Doctor`, `Patient`, and `Appointment` inherit from `db.Model` (SQLAlchemy's base class), automatically mapping classes to database tables and enabling built-in methods like `.query`, `.add`, and `.commit`.

- **Polymorphism**  
  The `__str__()` method is overridden in multiple classes, allowing Python’s `str(object)` function to correctly call the class-specific string representation, providing meaningful outputs.

---

## 📚 DSA Concepts Used

- **Queue Data Structure**  
  Appointment slots for doctors are managed using a queue, ensuring **First-In-First-Out (FIFO)** order. Patients are assigned the earliest available time slot automatically, maintaining fair and sequential appointment booking.

---

## 🛠️ Functional Overview

### 👤 Patient Registration
- Automatically assigns a unique patient ID (`p0001`, `p0002`, ...)
- Stores name and password securely in the database

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

## 🔐 User Registration
There are **no predefined doctors or patients** in this system. All users must register manually.
- Doctors receive an auto-generated ID like `d001`, `d002`, etc.
- Patients receive IDs like `p0001`, `p0002`, etc.
Once registered, users can log in using their assigned ID and chosen password.

---

## 📝 TODO (Improvements)
- Persistent storage with full database backup
- Forgot password / email validation
- Role-based admin panel
- Pagination for large appointment lists

---

## 📄 License
MIT License. Free to use and modify.
