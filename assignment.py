from flask import Flask, request, render_template, session, redirect, g
from os import urandom
import sqlite3 as sq

        
app = Flask(__name__)
sec_key=repr(urandom(24))
app.secret_key=sec_key
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sq.connect('hw12.db')
    return db
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
    global student_rows
    if 'username' not in session:
        return redirect('/login')
    else:
        g.d=g.db.cursor()
        g.d.execute('SELECT * FROM Students')
        student_rows=g.d.fetchall()
        return render_template("dashboard.html", methods=['GET', 'POST'], student_rows=student_rows)
@app.teardown_request
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
if __name__=="__main__":
    app.run(debug=True)