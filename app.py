from flask import Flask, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

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
    email = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10), nullable=False)

class Activity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    activity = db.Column(db.String(20), nullable=False)
    date = db.Column(db.String(20), nullable=False)
    meet = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Activity('{self.activity}', '{self.date}', '{self.meet}')"

@app.route("/")
def index():
    return render_template("name.html", title='Makan Gigi')

@app.route('/submit_name', methods=['POST'])
def submit_name():
    name = request.form['name']
    phone = request.form['phone']
    email = request.form['email']
    gender = request.form['gender']
    
    patient = Patient(name=name, phone=phone, email=email, gender=gender)
    db.session.add(patient)
    db.session.commit()
    
    return redirect(url_for('base', name=name, phone=phone, email=email, gender=gender))

@app.route('/base', methods=['GET', 'POST'])
def base():
    if request.method == 'POST':
        return redirect(url_for('ty'))
    return render_template("base.html", title='Base')

@app.route('/submit_reservation', methods=['POST'])
def submit_reservation():
    activity_name = request.form['activity']
    date = request.form['date']
    meet = request.form['time'] 

    reservation = Activity(activity=activity_name, date=date, meet=meet)
    db.session.add(reservation)
    db.session.commit()

    return redirect(url_for('ty'))

@app.route('/ty')
def ty():
    return render_template("ty.html", title='Thanks')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    return render_template('login.html', title='Admin Login')
    
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
