from flask import render_template, redirect, request, flash, url_for, Blueprint
from ..models.course_models import Course

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/course')
def course():
    courses = Course.get_all()
    colleges = Course.get_colleges()
    return render_template('course.html', course_list=courses, college=colleges)

@courses_bp.route('/add_course', methods=['POST'])
def add_course():
    course_code = request.form['course_code']
    course_name = request.form['course_name']
    college = request.form['college']

    try:
        Course.create(course_code, course_name, college)
        flash("Data Inserted Successfully")
    except:
        flash("Course code already exists. Please try another.")
    
    return redirect(url_for('courses.course'))

@courses_bp.route('/update_course', methods=['POST'])
def update_course():
    course_code = request.form['course_code']
    course_name = request.form['course_name']
    college = request.form['college']
    
    Course.update(course_code, course_name, college)
    flash("Data updated successfully")
    return redirect(url_for('courses.course'))

@courses_bp.route('/delete/course/<string:course_code>')
def delete_course(course_code):
    try:
        Course.delete(course_code)
        flash("Course has been deleted successfully")
    except:
        flash("Course that has students enrolled cannot be deleted")
    
    return redirect(url_for('courses.course'))

@courses_bp.route('/searchcourse', methods=['POST'])
def searchcourse():
    user_input = request.form['tableSearch']
    keyword = user_input.upper()
    result = Course.search(keyword)

    if result:
        colleges = Course.get_colleges()
        return render_template('course.html', course_list=result, college=colleges)
    else:
        flash("Result not found")
        return redirect(url_for('courses.course'))