from flask import Flask, render_template, url_for, redirect, request, flash
from SSIS import mysql
from . import student
from cloudinary.uploader import upload, destroy

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

@student.route('/')
def Index():
    cur = mysql.connection.cursor()
    cursor = mysql.connection.cursor()
    cur.execute("SELECT * FROM student_list")
    cursor.execute("SELECT * FROM course_list")
    course= cursor.fetchall()
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', student_list = data, course=course)

@student.route('/insert', methods = ['POST'])
def insert():
    stud_id = (request.form['stud_id']).strip()
    file = request.files.get('file')
    fname = request.form['fname']
    lname = request.form['lname']
    course = request.form['course']
    year_lvl = request.form['year_lvl']
    gender = request.form['gender']

    if request.method == "POST":
        try:
            result = upload(file.read(), public_id="ssis/{}".format(stud_id))
            url = result.get('url')
    
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student_list (stud_id, photo_link, fname, lname, year_lvl, gender, course_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (stud_id, url, fname, lname, year_lvl, gender, course))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
            return redirect(url_for('student.Index'))
        except:
            url = 'https://res.cloudinary.com/dkc0twhfx/image/upload/v1644327143/ssis/default_loflin.jpg'
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO student_list (stud_id, photo_link, fname, lname, year_lvl, gender, course_code) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                    (stud_id, url, fname, lname, year_lvl, gender, course))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
            return redirect(url_for('student.Index'))

@student.route('/delete/student/<string:stud_id>')
def delete(stud_id):
    destroy(public_id="ssis/{}".format(stud_id))
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM student_list WHERE stud_id=%s", (stud_id,))
    mysql.connection.commit()
    flash("Record has been deleted successfully")
    return redirect(url_for('student.Index'))

@student.route('/update', methods = ['POST', 'GET'])
def update():
    if request.method == 'POST':
        stud_id = (request.form['stud_id']).strip()
        fname = request.form['fname']
        lname = request.form['lname']
        course = request.form['course_code']
        year_lvl = request.form['year_lvl']
        gender = request.form['gender']

        try:
            file = request.files.get('file')
            result = upload(file.read(), public_id="ssis/{}".format(stud_id))
            url = result.get('url')
            cur = mysql.connection.cursor()
            cur.execute(
                """UPDATE student_list SET photo_link=%s, fname=%s, lname=%s, year_lvl=%s, gender=%s, course_code=%s WHERE stud_id=%s""",
                        (url, fname, lname, year_lvl, gender, course, stud_id))
            mysql.connection.commit()
            flash("Data updated successfully")
            return redirect(url_for('student.Index'))
        except:
            cur = mysql.connection.cursor()
            cur.execute(
                """UPDATE student_list SET fname=%s, lname=%s, year_lvl=%s, gender=%s, course_code=%s WHERE stud_id=%s""",
                        (fname, lname, year_lvl, gender, course, stud_id))
            mysql.connection.commit()
            flash("Data updated successfully")
            return redirect(url_for('student.Index'))

@student.route('/searchstudent', methods=['GET', 'POST'])
def searchstudent():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM student_list")
    students = cur.fetchall()
    user_input = request.form['tableSearch']
    keyword = user_input.upper()
    result = []

    for student in students:    
            student_allcaps = [str(info).upper() for info in student]
            if keyword in student_allcaps:
                result.append(student)
            result

    if len(result) !=0:
        return render_template('index.html', student_list=result)
    else:
        flash("Result not found")
        return redirect(url_for('student.Index'))