from flask import Flask, request, render_template, session, redirect, g, url_for
from os import urandom
import sqlite3 as sq

app = Flask(__name__)
sec_key = repr(urandom(24))
app.secret_key = sec_key


def get_db():
    db = getattr(g, 'database', None)
    if db is None:
        g.database = sq.connect('hw12.db')
        db = g.database
    return db


@app.route('/', methods=['GET', 'POST'])
def start():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    passw = request.form['passw']
    wrong_creds = False
    if username == 'admin' and passw == 'password':
        session['username'] = username
        return redirect(url_for("dashboard"))
    else:
        wrong_creds = True
        return render_template('/login.html', methods=['GET', 'POST'], wrong_creds=wrong_creds)


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    global student_rows
    if 'username' not in session:
        return redirect(url_for('/login'))
    else:
        db = get_db()
        cur = db.cursor()
        cur.execute('SELECT * FROM Students')
        student_rows = cur.fetchall()
        cur.execute('SELECT * FROM Quizzes')
        quiz_rows=cur.fetchall()
        return render_template("dashboard.html", methods=['GET', 'POST'], student_rows=student_rows, quiz_rows=quiz_rows)

@app.route('/student/add', methods=['GET', 'POST'])
def add_student():
    if request.method == 'GET':
        return render_template('student_add.html')
    elif request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('/login'))
        gdb = get_db()
        cur = gdb.cursor()
        cur.execute('insert into STUDENTS (F_NAME, L_NAME) values (?, ?)',
                     [request.form['f_name'], request.form['l_name']])
        gdb.commit()
    return redirect(url_for('dashboard'))
    
@app.route('/quiz/add', methods=['GET', 'POST'])
def add_quiz():
    if request.method == 'GET':
        return render_template('quiz_add.html')
    elif request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('/login'))
        gdb = get_db()
        cur = gdb.cursor()
        cur.execute('insert into Quizzes (SUBJECT, Q_NUM, DATE) values (?, ?, ?)',
                     [request.form['subject'], request.form['q_num'], request.form['date_given']])
        gdb.commit()
    return redirect(url_for('dashboard'))
@app.route('/student/<id_num>', methods=['GET'])
def results(id_num):
    if 'username' not in session:
        return redirect(url_for('/login'))
    else:
        gdb = get_db()
        cur = gdb.cursor()
        cur.execute('SELECT F_NAME,L_NAME,Q_ID,Subject,Date,Score FROM Students INNER JOIN results on STUDENTS.ST_ID=RESULTS.Student_ID INNER JOIN quizzes on RESULTS.Quiz_Id=QUIZZES.Q_Id WHERE st_id=(?)', [id_num])
        results_row=cur.fetchall()
        if results_row==[]:
            results_row=[("Sorry","no","information","available","for","student")]
            return render_template("student.html", methods=['GET'], results_row=results_row)
        else:
            return render_template("student.html", methods=['GET'], results_row=results_row)
@app.route('/results/add', methods=['GET', 'POST'])
def add_result():
    if request.method == 'GET':
        gdb = get_db()
        cur = gdb.cursor()
        cur.execute('SELECT St_ID from Students')
        student_list=cur.fetchall()
        cur.execute('SELECT Q_ID from Quizzes')
        quiz_list=cur.fetchall()
        return render_template('result_add.html', methods=['GET'], student_list=student_list, quiz_list=quiz_list)
    elif request.method == 'POST':
        if 'username' not in session:
            return redirect(url_for('/login'))
        else:
            gdb = get_db()
            cur = gdb.cursor()
            student_id=request.form['student_id']
            sid=student_id[1]
            quiz=request.form['quiz']
            qid=quiz[1]
            score=request.form['score']
            cur.execute('INSERT INTO RESULTS (SCORE, Student_ID, Quiz_ID) values (?,?,?)', [score,sid,qid])
            gdb.commit()
    return redirect(url_for('dashboard'))
            
            
@app.teardown_request
def close_connection(exception):
    db = getattr(g, 'database', None)
    if db is not None:
        db.close()

if __name__ == "__main__":
    app.run(debug=True)
