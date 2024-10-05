from flask import Flask, request, render_template, redirect, url_for, session
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)

db = SQLAlchemy(app)

class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    activities = relationship("Activity", back_populates="patient")

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    meet = db.Column(db.String(10), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patient.id'), nullable=False)

    patient = relationship("Patient", back_populates="activities")

    def __repr__(self):
        return f"Activity('{self.activity}', '{self.date}', '{self.meet}')"

@app.route("/")
def index():
    return render_template("name.html", title='Makan Gigi')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    name = request.form.get('name')
    phone = request.form.get('phone')
    email = request.form.get('email')
    gender = request.form.get('gender')
    
    patient = Patient(name=name, phone=phone, email=email, gender=gender)
    db.session.add(patient)
    db.session.commit()
    
    session['patient_id'] = patient.id
    
    return redirect(url_for('base'))

@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        return redirect(url_for('ty'))
    return render_template("base.html", title='Base')

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    activity_name = request.form['activity']
    date_str = request.form['date']
    meet = request.form['time']
    patient_id = session.get('patient_id')

    if not patient_id:
        return "Patient ID not found in session", 400

    patient = Patient.query.get(patient_id)
    if not patient:
        return "Patient not found", 404

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        return "Invalid date format", 400
        
    reservation = Activity(activity=activity_name, date=date, meet=meet, patient=patient)
    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('ty'))

@app.route('/ty')
def ty():
    return render_template("ty.html", title='Thanks')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == 'Admin' and password == 'IGSGACOR':
            return redirect(url_for('edit_database'))
        else:
            return render_template('login.html', error='Invalid username or password')
    return render_template('login.html')
    
@app.route('/edit_database')
def edit_database():
    patients = Patient.query.all()
    return render_template('edit_database.html', patients=patients)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True)
