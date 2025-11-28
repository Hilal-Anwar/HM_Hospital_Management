import random
from datetime import datetime, timedelta

from flask import Flask, render_template, redirect, url_for, request
from model import db, User, Department, Doctor, Patient, Appointments, Medicine, Treatments, DoctorsUnavailability
from sqlalchemy.orm import aliased

# create the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"
app.jinja_env.globals['datetime'] = __import__('datetime')
db.init_app(app)
today = datetime.today()
date_list = [(today + timedelta(days=i)).strftime('%d-%m-%Y') for i in range(7)]
with app.app_context():
    db.create_all()
    if not User.query.filter_by(username="admin").first():
        new_user = User(username="admin", password="admin", type="admin")
        db.session.add(new_user)
    if Department.query.count() == 0:
        departments = [
            Department(department_name="General Medicine",
                       department_description="""
                       General Medicine is the foundation of healthcare, providing comprehensive primary care for patients of all ages. It focuses on diagnosing, treating, and preventing a wide range of common illnesses and chronic conditions, such as diabetes, hypertension, infections, and respiratory issues. General physicians act as the first point of contact, offering holistic care and coordinating with specialists when needed. They emphasize patient education, lifestyle management, and early detection of diseases to promote long-term health. This department plays a vital role in managing overall wellness, ensuring continuity of care, and addressing both acute and preventive healthcare needs effectively.
                       """),
            Department(department_name="Cardiology",
                       department_description="Cardiology is the medical specialty focused on diagnosing, treating, and preventing diseases of the heart and blood vessels. It addresses conditions such as coronary artery disease, heart failure, arrhythmias, and hypertension. Cardiologists use advanced diagnostic tools like ECG, echocardiography, and cardiac catheterization to assess heart function and detect abnormalities. Treatment may involve medications, lifestyle changes, or procedures such as angioplasty and bypass surgery. Cardiology plays a vital role in managing cardiovascular health, reducing risk factors, and improving quality of life. With heart disease being a leading global health concern, this department ensures timely care and preventive strategies for patients."),
            Department(department_name="Neurology",
                       department_description="Neurology is the branch of medicine that deals with disorders of the brain, spinal cord, and nervous system. It focuses on diagnosing and treating conditions such as stroke, epilepsy, migraines, multiple sclerosis, Parkinson’s disease, and neuropathies. Neurologists use advanced techniques like MRI, CT scans, and EEG to assess neurological function and detect abnormalities. Treatment may involve medications, rehabilitation, and lifestyle adjustments to improve quality of life. Neurology plays a critical role in managing complex neurological disorders, preventing complications, and supporting patients with chronic conditions. This department ensures comprehensive care for both acute and long-term neurological health needs."),
            Department(department_name="Orthopedics",
                       department_description="Orthopedics is the medical specialty dedicated to diagnosing, treating, and preventing disorders of the bones, joints, muscles, ligaments, and tendons. It addresses conditions such as fractures, arthritis, spinal deformities, sports injuries, and congenital skeletal issues. Orthopedic care includes both surgical and non-surgical treatments, such as joint replacement, physiotherapy, and pain management. Specialists aim to restore mobility, reduce pain, and improve quality of life for patients of all ages. This department plays a crucial role in rehabilitation and recovery, helping individuals regain strength and function after injuries or chronic musculoskeletal conditions through advanced techniques and personalized care plans."),
            Department(department_name="Pediatrics",
                       department_description="Pediatrics is the branch of medicine dedicated to the health and well-being of infants, children, and adolescents. It focuses on diagnosing, treating, and preventing a wide range of conditions, including infections, developmental disorders, nutritional issues, and chronic illnesses. Pediatricians provide comprehensive care, including immunizations, growth monitoring, and guidance on physical and emotional development. They play a vital role in early detection of health problems and ensuring proper growth milestones. This department emphasizes preventive care, family education, and specialized treatment tailored to young patients, promoting healthy childhood and laying the foundation for lifelong wellness."),
            Department(department_name="Dermatology",
                       department_description="Dermatology is the medical specialty focused on diagnosing, treating, and preventing conditions related to the skin, hair, and nails. It addresses a wide range of issues, including acne, eczema, psoriasis, fungal infections, and skin allergies, as well as cosmetic concerns like pigmentation and aging. Dermatologists also play a crucial role in detecting and managing serious conditions such as skin cancer. Treatments may include medications, topical therapies, laser procedures, and minor surgeries. This department emphasizes both medical and aesthetic care, helping patients maintain healthy skin and overall confidence while preventing complications through early detection and personalized treatment plans."),
            Department(department_name="Gynecology",
                       department_description="Gynecology is the medical specialty focused on women’s reproductive health, covering the diagnosis, treatment, and prevention of conditions affecting the uterus, ovaries, fallopian tubes, and related structures. It addresses issues such as menstrual disorders, hormonal imbalances, infertility, infections, and menopause. Gynecologists also provide essential preventive care, including Pap smears, cancer screenings, and contraceptive counseling. This department plays a vital role in maternal health, offering guidance during pregnancy and postpartum care. With an emphasis on both physical and emotional well-being, gynecology ensures comprehensive care for women at all stages of life, promoting reproductive health and overall wellness."),
            Department(department_name="Oncology",
                       department_description="Oncology is the medical specialty dedicated to the prevention, diagnosis, and treatment of cancer. It addresses various types of malignancies affecting organs and tissues throughout the body. Oncologists use advanced diagnostic tools such as biopsies, imaging, and molecular testing to identify cancer stages and types. Treatment options include chemotherapy, radiation therapy, immunotherapy, and surgical interventions, often combined for optimal outcomes. Oncology also emphasizes palliative care and psychological support to improve patients’ quality of life. This department plays a critical role in cancer research, early detection, and personalized treatment plans, aiming to reduce mortality and enhance long-term survival rates."),
            Department(department_name="Radiology",
                       department_description="Radiology is the medical specialty that uses imaging technologies to diagnose and monitor diseases and injuries within the body. It employs advanced tools such as X-rays, CT scans, MRI, ultrasound, and mammography to provide detailed internal views without invasive procedures. Radiologists interpret these images to detect fractures, tumors, infections, and other abnormalities, aiding accurate diagnosis and treatment planning. This department plays a vital role in early disease detection, guiding surgical interventions, and monitoring recovery. Radiology ensures precision in healthcare by combining cutting-edge imaging techniques with expert analysis, making it an essential component of modern medical practice."),
            Department(department_name="Emergency Medicine",
                       department_description="Emergency Medicine is the medical specialty dedicated to providing immediate care for patients with acute illnesses or injuries that require urgent attention. It covers a wide range of emergencies, including trauma, heart attacks, strokes, respiratory distress, and severe infections. Emergency physicians are trained to stabilize patients, perform life-saving interventions, and coordinate further treatment. This department operates 24/7, ensuring rapid diagnosis and management using advanced equipment and protocols. Emergency Medicine plays a critical role in reducing mortality and preventing complications by delivering prompt, efficient, and comprehensive care during critical situations, making it an essential pillar of modern healthcare systems."),
            Department(department_name="Psychiatry",
                       department_description="Psychiatry is the medical specialty focused on diagnosing, treating, and preventing mental health disorders. It addresses conditions such as depression, anxiety, bipolar disorder, schizophrenia, and substance abuse. Psychiatrists use a combination of clinical evaluation, psychotherapy, and medications to manage symptoms and improve emotional well-being. This department plays a vital role in promoting mental health, reducing stigma, and supporting patients through personalized care plans. Psychiatry also emphasizes early intervention, crisis management, and rehabilitation to help individuals lead productive lives. By integrating psychological and medical approaches, it ensures comprehensive care for complex behavioral and emotional challenges.")
        ]
        db.session.add_all(departments)

    # List of medicines
    medicine_names = [
        "Acetaminophen", "Adderall", "Amitriptyline", "Amlodipine", "Amoxicillin",
        "Ativan", "Atorvastatin", "Azithromycin", "Benzonatate", "Biktarvy",
        "Botox", "Brilinta", "Bunavail", "Buprenorphine", "Cephalexin",
        "Ciprofloxacin", "Citalopram", "Clindamycin", "Clonazepam", "Cyclobenzaprine",
        "Cymbalta", "Doxycycline", "Dupixent", "Entresto", "Entyvio", "Farxiga",
        "Fentanyl Patch", "Gabapentin", "Gemtesa", "Humira", "Hydrochlorothiazide",
        "Ibuprofen", "Imbruvica", "Januvia", "Jardiance", "Keytruda", "Lexapro",
        "Lisinopril", "Lofexidine", "Loratadine", "Loratadine for Dogs", "Lyrica",
        "Melatonin", "Meloxicam", "Metformin", "Methadone", "Methotrexate",
        "Metoprolol", "Mounjaro", "Naltrexone", "Naproxen", "Narcan", "Nurtec",
        "Omeprazole", "Opdivo", "Otezla", "Ozempic", "Pantoprazole", "Plan B",
        "Prednisone", "Probuphine", "Qulipta", "Quviviq", "Rybelsus", "Sublocade",
        "Sunlenca", "Tepezza", "Tramadol", "Trazodone", "Viagra", "Vraylar",
        "Wegovy", "Wellbutrin", "Xanax", "Yervoy", "Zepbound", "Zubsolv"
    ]

    if Medicine.query.count() == 0:
        for name in medicine_names:
            medicine = Medicine(medicine_name=name)
            db.session.add(medicine)

    db.session.commit()


@app.route('/')
def index():
    return render_template("login.html", error=False)


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.id)).scalars()
    return render_template("list.html", users=users)


@app.route("/user/login", methods=["GET", "POST"])
def login():
    try:
        if request.method == "POST":
            u_name = request.form["username"]
            u_pass = request.form["password"]
            user = User.query.filter_by(username=u_name, password=u_pass).first()
            if user:
                if u_name == "admin" and u_pass == "admin" and user.type == "admin":
                    return redirect(url_for("admin_view"))
                elif user.type == "doctor":
                    return redirect(
                        url_for("doctor_view", doctor_id=Doctor.query.filter_by(user_id=user.id).first().doctor_id))
                elif user.type == "patient":
                    return redirect(
                        url_for("patient_view", patient_id=Patient.query.filter_by(user_id=user.id).first().patient_id))
            else:
                return render_template("login.html", error=True)
    except Exception as e:
        return render_template("error.html")


@app.route("/doctor/<int:user_id>/<int:dr_id>/delete")
def doctor_delete(user_id, dr_id):
    user = db.get_or_404(User, user_id)
    doctor = db.session.query(Doctor).get(dr_id)
    appointments = Appointments.query.filter_by(doctor_id=dr_id).all()
    Treatments.query.filter_by(doctor_id=dr_id).delete()
    for apt in appointments:
        treatments = Treatments.query.filter_by(doctor_id=apt.doctor_id).all()
        for treatment in treatments:
            db.session.delete(treatment)
        db.session.delete(apt)
        db.session.commit()
    print(user, doctor, appointments)
    db.session.delete(doctor)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_view"))


@app.route("/user/admin", methods=["GET", "POST"])
def admin_view():
    a = aliased(Appointments)
    p = aliased(Patient)
    d = aliased(Doctor)
    dept = aliased(Department)
    token = ''
    search_dep = None
    if request.method == "POST":
        token = request.form['valueSearch']
        if len(token) > 0:
            search_dep = Department.query.filter_by(department_name=token).first()
    query = (
        db.session.query(
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            a.patient_id,
            p.patient_name,
            d.user_id,
            d.doctor_name,
            d.experience,
            dept.department_name,
            dept.department_description
        )
        .join(p, a.patient_id == p.patient_id)
        .join(d, a.doctor_id == d.doctor_id)
        .join(dept, a.department_id == dept.department_id)
    )

    results = query.all()
    treatment = db.session.query(Treatments.doctor_id, Treatments.patient_id, Treatments.test_done,
                                 Treatments.diagnosis, Treatments.medicine_dose, Treatments.prescription,
                                 Treatments.visit_type).all()

    if not token.strip():
        patients = Patient.query.all()
        doctors = Doctor.query.all()
    else:
        patients = Patient.query.filter(Patient.patient_name.ilike(f"{token}%")).all()
        doctors = Doctor.query.filter(Doctor.doctor_name.ilike(f"{token}%")).all()
        if not patients:
            patients = Patient.query.all()
        if not doctors:
            if search_dep and search_dep.department_id:
                doctors = Doctor.query.filter_by(department_id=search_dep.department_id).all()
            else:
                doctors = Doctor.query.all()

    return render_template("admin_view.html", departments=Department.query.all(),
                           doctors=doctors,
                           patients=patients,
                           appointments=results, treatment=treatment, users=User.query.all())


@app.route("/patient/<int:patient_id>")
def patient_view(patient_id):
    a = aliased(Appointments)
    p = aliased(Patient)
    d = aliased(Doctor)
    dept = aliased(Department)

    query = (
        db.session.query(
            a.appointment_id,
            a.appointment_date,
            a.appointment_time,
            p.patient_name,
            p.patient_id,
            d.doctor_name,
            d.experience,
            dept.department_name,
            a.status,
            a.doctor_id,
            dept.department_description
        )
        .join(p, a.patient_id == p.patient_id)
        .join(d, a.doctor_id == d.doctor_id)
        .join(dept, a.department_id == dept.department_id).where(a.patient_id == patient_id)
    )

    results = query.all()

    return render_template("patient.html", patient=Patient.query.filter_by(patient_id=patient_id).first(),
                           departments=Department.query.all(), appointments=results,
                           treatment=Treatments.query.filter_by(patient_id=patient_id).all())


@app.route("/doctor/<int:doctor_id>")
def doctor_view(doctor_id):
    booked_appointment = db.session.query(
        Patient.patient_name,
        Patient.patient_id,
        Appointments.appointment_date,
        Appointments.appointment_id,
        Appointments.appointment_time,
        Appointments.status
    ).join(Appointments, Patient.patient_id == Appointments.patient_id).filter(
        Appointments.doctor_id == doctor_id)
    dr = Doctor.query.filter_by(doctor_id=doctor_id).first()
    treatment = (
        db.session.query(Treatments.prescription, Treatments.medicine_dose,
                         Treatments.diagnosis, Treatments.test_done,
                         Treatments.visit_type, Treatments.patient_id).filter(
            Treatments.doctor_id == doctor_id).all())
    doctors_availability = get_doctor_availability(doctor_id)
    patients = booked_appointment.group_by(
        Patient.patient_name,
        Patient.patient_id)
    return render_template("doctor.html", doctor=dr,
                           booked_appointment=booked_appointment.filter_by(status='booked').all(),
                           medicine_name=Medicine.query.all(), doctor_dept=Department.query.filter_by(
            department_id=dr.department_id).first().department_name, treatment=treatment,
                           doctors_availability=doctors_availability, patients=patients)


def get_doctor_availability(doctor_id):
    doctors_availability = dict(dict())
    for d in date_list:
        record = (
            db.session.query(DoctorsUnavailability)
            .filter_by(date=datetime.strptime(d, "%d-%m-%Y").date(), doctor_id=doctor_id)
            .one_or_none()
        )
        if record:
            doctors_availability[d] = {"slot1": record.slot1, "slot2": record.slot2}
        else:
            doctors_availability[d] = {"slot1": 1, "slot2": 1}
    return doctors_availability


@app.route("/user/register", methods=["GET", "POST"])
def user_register():
    try:
        if request.method == "POST":
            user = User(
                username=request.form["username"],
                password=request.form["password"],
                type="patient"
            )
            db.session.add(user)
            db.session.commit()
            patient = Patient(
                user_id=user.id,
                patient_name=request.form["username"],
                status='normal'
            )
            db.session.add(patient)
            db.session.commit()
            return render_template("patient.html", patient=patient, departments=Department.query.all(),
                                   doctors=Doctor.query.all())
        else:
            return render_template("register.html")
    except Exception as e:
        return render_template("error.html")


@app.route("/doctor/<int:dr_id>/edit", methods=["POST"])
def doctor_edit(dr_id):
    doctor = db.session.query(Doctor).get(dr_id)
    user = User.query.filter_by(id=doctor.user_id).first()
    print(doctor, user)
    if request.method == "POST":
        doctor.experience = request.form["experience"]
        user.password = request.form["password"]
        db.session.commit()
    return redirect(url_for("admin_view"))


@app.route("/patient/<int:patient_id>/edit/<string:name_of_user>", methods=["POST"])
def patient_edit(patient_id, name_of_user):
    patient = Patient.query.filter_by(patient_id=patient_id).first()
    user = User.query.filter_by(id=patient.user_id).first()
    user.password = request.form["password"]
    db.session.commit()
    if name_of_user == 'admin':
        return redirect(url_for("admin_view"))
    else:
        return redirect(url_for("patient_view", patient_id=patient_id))


@app.route("/patient/<int:user_id>/<int:patient_id>/delete")
def patient_delete(user_id, patient_id):
    user = db.get_or_404(User, user_id)
    patient = db.session.query(Patient).get(patient_id)
    appointments = Appointments.query.filter_by(patient_id=patient_id).all()
    for apt in appointments:
        treatments = Treatments.query.filter_by(patient_id=apt.patient_id).all()
        for treatment in treatments:
            db.session.delete(treatment)
        db.session.delete(apt)
        db.session.commit()
    print(user, patient, appointments)
    db.session.delete(patient)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("admin_view"))


@app.route("/user/add_doctor", methods=["GET", "POST"])
def add_doctor():
    if request.method == "POST":
        print(request.form["doctor_name"])
        print(request.form["experience"])
        print(Department.query.filter_by(department_id=request.form.get('department_id')).first().department_name)
        print(request.form["password"])
        user = User(
            username=request.form["doctor_name"],
            password=request.form["password"],
            type="doctor"
        )
        db.session.add(user)
        db.session.commit()
        doctor = Doctor(
            doctor_name=request.form["doctor_name"],
            user_id=user.id,
            department_id=request.form.get('department_id'),
            experience=request.form["experience"],
            status="normal"
        )
        db.session.add(doctor)
        db.session.commit()
    return render_template("admin_view.html", departments=Department.query.all(),
                           doctors=Doctor.query.all(), patients=Patient.query.all())


@app.route('/user/<int:dpt_id>/<int:p_id>/department', methods=["GET", "POST"])
def department(dpt_id, p_id):
    print(dpt_id, p_id)
    dept = Department.query.filter_by(department_id=dpt_id).first()
    doctors = Doctor.query.filter(Doctor.department_id == dpt_id)
    list_of_doctors_availability = dict()
    for doctor in doctors:
        list_of_doctors_availability[doctor.doctor_id] = get_doctor_availability(doctor.doctor_id)
    return render_template("department.html", department=dept, patient=p_id,
                           doctors=Doctor.query.filter(Doctor.department_id == dpt_id).all(),
                           doctors_availability=list_of_doctors_availability)


@app.route('/user/dept', methods=["POST"])
def department_add():
    if request.method == "POST":
        dept_name = request.form["dept_name"]
        dept_dis = request.form["dept_description"]
        new_department = Department(
            department_name=dept_name,
            department_description=dept_dis)
        db.session.add(new_department)
        db.session.commit()
    return redirect(url_for("admin_view"))


@app.route('/<string:user_type>/<int:appointment_id>/<int:ids>', methods=["POST"])
def cancel_appointment(user_type, appointment_id, ids):
    print(appointment_id, ids)
    if request.method == "POST":
        appoint = Appointments.query.filter_by(appointment_id=appointment_id).first()
        appoint.status = 'canceled'
        db.session.commit()
        print(appoint)
    if user_type == "patient":
        return redirect(url_for("patient_view", patient_id=ids))
    else:
        return redirect(url_for("doctor_view", doctor_id=ids))


@app.route('/user/<int:pat_id>/<int:dr_id>/<int:dept_id>/book_slot', methods=['POST'])
def book_appointment(pat_id, dr_id, dept_id):
    doctor = Doctor.query.filter_by(doctor_id=dr_id).first()
    dept = Department.query.filter_by(department_id=dept_id).first()
    selected_slot = request.form.get('selected_slot')
    print(pat_id, doctor.doctor_name, dept.department_name)
    print(selected_slot.split('|')[0], selected_slot.split('|')[1])
    appointment = Appointments(
        patient_id=pat_id,
        doctor_id=doctor.doctor_id,
        department_id=dept.department_id,
        status="booked",
        appointment_date=datetime.strptime(selected_slot.split('|')[1], '%d-%m-%Y'),
        appointment_time=selected_slot.split('|')[0],
    )
    db.session.add(appointment)
    db.session.commit()
    return redirect(url_for("patient_view", patient_id=pat_id))


@app.route('/diagnose/<int:dr_id>/<int:appointment_id>/<int:patient_id>', methods=['POST'])
def diagnose(dr_id, appointment_id, patient_id):
    m1 = request.form.get('medicines_id1')
    m2 = request.form.get('medicines_id2')
    m3 = request.form.get('medicines_id3')
    d1 = request.form.get('dose_1')
    d2 = request.form.get('dose_2')
    d3 = request.form.get('dose_3')
    if m1 and d1:
        m1 = m1 + ":" + d1
    if m2 and d2:
        m2 = m2 + ":" + d2
    if m3 and d3:
        m3 = m3 + ":" + d3
    treatments = Treatments(
        doctor_id=dr_id,
        patient_id=patient_id,
        visit_type=request.form.get('vist_type'),
        test_done=request.form.get('test_done'),
        diagnosis=request.form.get('diagnosis'),
        prescription=request.form.get('prescription'),
        medicine_dose=m1 + "," + m2 + "," + m3
    )
    db.session.add(treatments)
    appointment = Appointments.query.filter_by(appointment_id=appointment_id).first()
    appointment.status = "completed"
    db.session.commit()
    print("done")
    return redirect(url_for("doctor_view", doctor_id=dr_id))


@app.route('/doctor/book_slot/<int:dr_id>', methods=['POST'])
def save_unavailability(dr_id):
    selected_slot = request.form.getlist('selected_slot')
    print(selected_slot)
    for slot in selected_slot:
        if slot.split('|')[0] == 'slot1':
            upsert_doctors_unavailability(slot.split('|')[1], dr_id, slot1=0)
        if slot.split('|')[0] == 'slot2':
            upsert_doctors_unavailability(slot.split('|')[1], dr_id, slot2=0)
    return "😂😘❤️"


def upsert_doctors_unavailability(date_input, doctor_id, slot1=None, slot2=None):
    date = datetime.strptime(date_input, "%d-%m-%Y").date()
    record = (
        db.session.query(DoctorsUnavailability)
        .filter_by(date=date, doctor_id=doctor_id)
        .one_or_none()
    )
    if record:
        print(slot1, slot2)
        print(record.slot1, record.slot2)
        if record.slot1 == 1 and slot1 is not None:
            record.slot1 = 0
        elif record.slot1 == 0 and slot1 is not None:
            record.slot1 = 1
        if record.slot2 == 1 and slot2 is not None:
            record.slot2 = 0
        elif record.slot2 == 0 and slot2 is not None:
            record.slot2 = 1
        db.session.add(record)
        print(record.slot1, record.slot2)
    else:
        # Insert new
        record = DoctorsUnavailability(
            date=date,
            doctor_id=doctor_id,
            slot1=slot1,
            slot2=slot2,
        )
        db.session.add(record)
    db.session.commit()


if __name__ == '__main__':
    app.run()
