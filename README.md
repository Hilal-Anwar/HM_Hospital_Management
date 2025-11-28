# Healthcare Appointment System

A web application for managing healthcare appointments, doctors, patients, and departments. Built with **Flask**, **SQLAlchemy**, **SQLite** and **Bootstrap**.

## Features
- User authentication (**Admin**, **Doctor**, **Patient**)
- Admin dashboard for managing users, departments, and appointments
- Patient dashboard for booking appointments and viewing treatments
- Doctor dashboard for managing availability and recording diagnoses
- Department and medicine management

## Requirements
- Python 3.8+
- Flask
- SQLAlchemy

Install dependencies:
```bash
pip install flask sqlalchemy
```

## How to Run
1. **Clone the repository**:
   ```bash
   git clone https://github.com/Hilal-Anwar/HM_Hospital_Management
   cd HM_Hospital_Management
   ```

2. **Set up the database**:
   The app uses SQLite by default. Tables will be created automatically on first run.

3. **Run the Flask app**:
   ```bash
   flask --app controller run --host=0.0.0.0
   ```
   By default, the app runs on:
   ```
   http://localhost:5000
   ```

## Default Admin Login
```
Username: admin
Password: admin
```

## Project Structure
```
project/
│── controller.py      # Main Flask application
│── model.py           # Database models
│── templates/         # HTML templates
```

##  Endpoints
- `/` – Login page
- `/user/admin` – Admin dashboard
- `/patient/<id>` – Patient dashboard
- `/doctor/<id>` – Doctor dashboard

