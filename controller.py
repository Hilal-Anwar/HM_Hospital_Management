from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import Mapped, mapped_column
from model import db, User, Department

# create the app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.sqlite3"

db.init_app(app)

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
            Department(department_name="Cardiology", department_description="Cardiology is the medical specialty focused on diagnosing, treating, and preventing diseases of the heart and blood vessels. It addresses conditions such as coronary artery disease, heart failure, arrhythmias, and hypertension. Cardiologists use advanced diagnostic tools like ECG, echocardiography, and cardiac catheterization to assess heart function and detect abnormalities. Treatment may involve medications, lifestyle changes, or procedures such as angioplasty and bypass surgery. Cardiology plays a vital role in managing cardiovascular health, reducing risk factors, and improving quality of life. With heart disease being a leading global health concern, this department ensures timely care and preventive strategies for patients."),
            Department(department_name="Neurology", department_description="Neurology is the branch of medicine that deals with disorders of the brain, spinal cord, and nervous system. It focuses on diagnosing and treating conditions such as stroke, epilepsy, migraines, multiple sclerosis, Parkinson’s disease, and neuropathies. Neurologists use advanced techniques like MRI, CT scans, and EEG to assess neurological function and detect abnormalities. Treatment may involve medications, rehabilitation, and lifestyle adjustments to improve quality of life. Neurology plays a critical role in managing complex neurological disorders, preventing complications, and supporting patients with chronic conditions. This department ensures comprehensive care for both acute and long-term neurological health needs."),
            Department(department_name="Orthopedics", department_description="Orthopedics is the medical specialty dedicated to diagnosing, treating, and preventing disorders of the bones, joints, muscles, ligaments, and tendons. It addresses conditions such as fractures, arthritis, spinal deformities, sports injuries, and congenital skeletal issues. Orthopedic care includes both surgical and non-surgical treatments, such as joint replacement, physiotherapy, and pain management. Specialists aim to restore mobility, reduce pain, and improve quality of life for patients of all ages. This department plays a crucial role in rehabilitation and recovery, helping individuals regain strength and function after injuries or chronic musculoskeletal conditions through advanced techniques and personalized care plans."),
            Department(department_name="Pediatrics", department_description="Pediatrics is the branch of medicine dedicated to the health and well-being of infants, children, and adolescents. It focuses on diagnosing, treating, and preventing a wide range of conditions, including infections, developmental disorders, nutritional issues, and chronic illnesses. Pediatricians provide comprehensive care, including immunizations, growth monitoring, and guidance on physical and emotional development. They play a vital role in early detection of health problems and ensuring proper growth milestones. This department emphasizes preventive care, family education, and specialized treatment tailored to young patients, promoting healthy childhood and laying the foundation for lifelong wellness."),
            Department(department_name="Dermatology", department_description="Dermatology is the medical specialty focused on diagnosing, treating, and preventing conditions related to the skin, hair, and nails. It addresses a wide range of issues, including acne, eczema, psoriasis, fungal infections, and skin allergies, as well as cosmetic concerns like pigmentation and aging. Dermatologists also play a crucial role in detecting and managing serious conditions such as skin cancer. Treatments may include medications, topical therapies, laser procedures, and minor surgeries. This department emphasizes both medical and aesthetic care, helping patients maintain healthy skin and overall confidence while preventing complications through early detection and personalized treatment plans."),
            Department(department_name="Gynecology", department_description="Gynecology is the medical specialty focused on women’s reproductive health, covering the diagnosis, treatment, and prevention of conditions affecting the uterus, ovaries, fallopian tubes, and related structures. It addresses issues such as menstrual disorders, hormonal imbalances, infertility, infections, and menopause. Gynecologists also provide essential preventive care, including Pap smears, cancer screenings, and contraceptive counseling. This department plays a vital role in maternal health, offering guidance during pregnancy and postpartum care. With an emphasis on both physical and emotional well-being, gynecology ensures comprehensive care for women at all stages of life, promoting reproductive health and overall wellness."),
            Department(department_name="Oncology", department_description="Oncology is the medical specialty dedicated to the prevention, diagnosis, and treatment of cancer. It addresses various types of malignancies affecting organs and tissues throughout the body. Oncologists use advanced diagnostic tools such as biopsies, imaging, and molecular testing to identify cancer stages and types. Treatment options include chemotherapy, radiation therapy, immunotherapy, and surgical interventions, often combined for optimal outcomes. Oncology also emphasizes palliative care and psychological support to improve patients’ quality of life. This department plays a critical role in cancer research, early detection, and personalized treatment plans, aiming to reduce mortality and enhance long-term survival rates."),
            Department(department_name="Radiology", department_description="Radiology is the medical specialty that uses imaging technologies to diagnose and monitor diseases and injuries within the body. It employs advanced tools such as X-rays, CT scans, MRI, ultrasound, and mammography to provide detailed internal views without invasive procedures. Radiologists interpret these images to detect fractures, tumors, infections, and other abnormalities, aiding accurate diagnosis and treatment planning. This department plays a vital role in early disease detection, guiding surgical interventions, and monitoring recovery. Radiology ensures precision in healthcare by combining cutting-edge imaging techniques with expert analysis, making it an essential component of modern medical practice."),
            Department(department_name="Emergency Medicine", department_description="Emergency Medicine is the medical specialty dedicated to providing immediate care for patients with acute illnesses or injuries that require urgent attention. It covers a wide range of emergencies, including trauma, heart attacks, strokes, respiratory distress, and severe infections. Emergency physicians are trained to stabilize patients, perform life-saving interventions, and coordinate further treatment. This department operates 24/7, ensuring rapid diagnosis and management using advanced equipment and protocols. Emergency Medicine plays a critical role in reducing mortality and preventing complications by delivering prompt, efficient, and comprehensive care during critical situations, making it an essential pillar of modern healthcare systems."),
            Department(department_name="Psychiatry", department_description="Psychiatry is the medical specialty focused on diagnosing, treating, and preventing mental health disorders. It addresses conditions such as depression, anxiety, bipolar disorder, schizophrenia, and substance abuse. Psychiatrists use a combination of clinical evaluation, psychotherapy, and medications to manage symptoms and improve emotional well-being. This department plays a vital role in promoting mental health, reducing stigma, and supporting patients through personalized care plans. Psychiatry also emphasizes early intervention, crisis management, and rehabilitation to help individuals lead productive lives. By integrating psychological and medical approaches, it ensures comprehensive care for complex behavioral and emotional challenges.")
        ]
        db.session.add_all(departments)
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
                    return render_template("admin_view.html")
                elif user.type == "patient":
                    return render_template("patient.html")
            else:
                return render_template("login.html", error=True)
    except Exception as e:
        return render_template("error.html")


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
            return render_template("patient.html")
        else:
            return render_template("register.html")
    except Exception as e:
        return render_template("error.html")


@app.route("/user/<int:id>/edit", methods=["POST", "GET"])
def user_edit(id):
    user = db.session.query(User).get(id)
    if request.method == "POST":
        user.username = request.form["username"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("user_list"))
    return render_template("edit.html", user=user)


@app.route("/user/<int:id>/delete")
def user_delete(id):
    user = db.get_or_404(User, id)
    print(user, request.method)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("user_list"))


if __name__ == '__main__':
    app.run()
