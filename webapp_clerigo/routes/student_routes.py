from flask import render_template, url_for, redirect, request, flash, Blueprint
from ..models.student_models import Student

students_bp = Blueprint('students', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@students_bp.route('/')
def Index():
    students = Student.get_all()
    courses = Student.get_courses()
    return render_template('index.html', student_list=students, course=courses)

@students_bp.route('/insert', methods=['POST'])
def insert():
    stud_id = request.form['stud_id'].strip()
    file = request.files.get('file')
    fname = request.form['fname']
    lname = request.form['lname']
    course = request.form['course']
    year_lvl = request.form['year_lvl']
    gender = request.form['gender']

    try:
        if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            url = Student.upload_photo(file, stud_id)
        else:
            raise Exception("Invalid file type")
    except:
        url = 'https://res.cloudinary.com/dkc0twhfx/image/upload/v1644327143/ssis/default_loflin.jpg'
    
    Student.create(stud_id, url, fname, lname, year_lvl, gender, course)
    flash("Data Inserted Successfully")
    return redirect(url_for('students.Index'))

@students_bp.route('/delete/student/<string:stud_id>')
def delete(stud_id):
    Student.delete_photo(stud_id)
    Student.delete(stud_id)
    flash("Record has been deleted successfully")
    return redirect(url_for('students.Index'))

@students_bp.route('/update', methods=['POST'])
def update():
    stud_id = request.form['stud_id'].strip()
    fname = request.form['fname']
    lname = request.form['lname']
    course = request.form['course_code']
    year_lvl = request.form['year_lvl']
    gender = request.form['gender']
    file = request.files.get('file')

    try:
        if file and file.filename.split('.')[-1].lower() in ALLOWED_EXTENSIONS:
            url = Student.upload_photo(file, stud_id)
            Student.update_with_photo(url, fname, lname, year_lvl, gender, course, stud_id)
        else:
            raise Exception("No valid file provided")
    except:
        Student.update_without_photo(fname, lname, year_lvl, gender, course, stud_id)
    
    flash("Data updated successfully")
    return redirect(url_for('students.Index'))

@students_bp.route('/searchstudent', methods=['POST'])
def searchstudent():
    user_input = request.form['tableSearch']
    keyword = user_input.upper()
    result = Student.search(keyword)

    if result:
        return render_template('index.html', student_list=result)
    else:
        flash("Result not found")
        return redirect(url_for('students.Index'))
