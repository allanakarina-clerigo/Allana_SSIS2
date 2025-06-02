from flask import render_template, redirect, request, flash, url_for
from flask import Blueprint
from ..models.college_models import College

colleges_bp = Blueprint('colleges', __name__)

@colleges_bp.route('/college')
def college():
    colleges = College.get_all()
    return render_template('college.html', college_list=colleges)

@colleges_bp.route('/add_college', methods=['POST'])
def add_college():
    college_code = request.form['college_code']
    college_name = request.form['college_name']

    try:
        College.create(college_code, college_name)
        flash("Data Inserted Successfully")
    except:
        flash("College code already exists. Please try another.")
    
    return redirect(url_for('colleges.college'))

@colleges_bp.route('/update_college', methods=['POST'])
def update_college():
    college_code = request.form['college_code']
    college_name = request.form['college_name']
    
    College.update(college_code, college_name)
    flash("Data updated successfully")
    return redirect(url_for('colleges.college'))

@colleges_bp.route('/delete/college/<string:college_code>')
def delete_college(college_code):
    try:
        College.delete(college_code)
        flash("College has been deleted successfully")
    except:
        flash("College that has existing courses cannot be deleted")
    
    return redirect(url_for('colleges.college'))

@colleges_bp.route('/searchcollege', methods=['POST'])
def searchcollege():
    user_input = request.form['tableSearch']
    keyword = user_input.upper()
    result = College.search(keyword)

    if result:
        return render_template('college.html', college_list=result)
    else:
        flash("Result not found")
        return redirect(url_for('colleges.college'))