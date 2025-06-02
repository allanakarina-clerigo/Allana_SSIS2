from logging import warning
from flask import Flask, render_template, url_for, redirect, request, flash
from SSIS import mysql
from . import colleges

@colleges.route('/college')
def college():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM college_list")
    data = cur.fetchall()
    cur.close()

    return render_template('college.html', college_list = data)

@colleges.route('/add_college', methods = ['POST'])
def add_college():
    if request.method == "POST":
        college_code = request.form['college_code']
        college_name = request.form['college_name']

        try:
            cur = mysql.connection.cursor()
            cur.execute("INSERT INTO college_list (college_code, college_name) VALUES (%s, %s)",
                            (college_code, college_name))
            mysql.connection.commit()
            flash("Data Inserted Successfully")
            return redirect(url_for('college.college'))
        except:
            flash("College code already exist. Please try another.")
            return redirect(url_for('college.college'))

@colleges.route('/update_college', methods = ['POST', 'GET'])
def update_college():
    if request.method == 'POST':
        college_code = request.form['college_code']
        college_name = request.form['college_name']
        cur = mysql.connection.cursor()
        cur.execute(
            """UPDATE college_list SET college_name=%s WHERE college_code=%s""",
            (college_name, college_code))
        mysql.connection.commit()
        flash("Data updated successfully")
        return redirect(url_for('college.college'))

@colleges.route('/delete/college/<string:college_code>', methods = ['GET'])
def delete_college(college_code):
    try:
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM college_list WHERE college_code=%s", (college_code,))
        mysql.connection.commit()
        flash("College has been deleted successfully")
        return redirect(url_for('college.college'))
    except:
        flash("College that has existing courses cannot be deleted.")
        return redirect(url_for('college.college'))

@colleges.route('/searchcollege', methods=['GET', 'POST'])
def searchstudent():
    cur = mysql.connection.cursor()
    cur.execute("SELECT  * FROM college_list")
    colleges = cur.fetchall()
    user_input = request.form['tableSearch']
    keyword = user_input.upper()
    result = []

    for college in colleges:    
            student_allcaps = [str(info).upper() for info in college]
            if keyword in student_allcaps:
                result.append(college)
            result

    if len(result) !=0:
        return render_template('college.html', college_list=result)
    else:
        flash("Result not found")
        return redirect(url_for('college.college'))