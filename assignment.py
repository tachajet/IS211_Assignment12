from flask import Flask, request, render_template, session, redirect
from os import urandom
import sqlite3 as sq
app = Flask(__name__)
sec_key=repr(urandom(24))
app.secret_key=sec_key
@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('login.html')
@app.route('/login', methods = ['POST'])
def login():
    username=request.form['username']
    passw=request.form['passw']
    wrong_creds=False
    if username=='admin' and passw=='password':
        session['username'] = username
        return render_template("dashboard.html")
    else:
        wrong_creds=True
        return render_template('/login.html', methods=['GET', 'POST'], wrong_creds=wrong_creds)
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    data_link=sq.connect('hw12.db')
    d=data_link.cursor()
    d.execute('SELECT * FROM Students')
    student_rows=d.fetchall()
    if 'username' not in session:
        return redirect('/login')
    else:
        return render_template("dashboard.html", methods=['GET', 'POST'], student_rows=student_rows)
if __name__=="__main__":
    app.run(debug=True)