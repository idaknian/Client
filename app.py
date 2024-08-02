from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS

app = Flask(__name__)
app.config['SECRET_KEY'] = 'SECRET'
CORS(app)

@app.route("/")
def index():
    return render_template("name.html", title='Makan Gigi')


@app.route('/base', methods=['POST'])
def submit_name():
    name = request.form['name']
    return render_template("base.html", title='Welcome', name=name)

if __name__ == '__main__':
    app.run(debug=True)
