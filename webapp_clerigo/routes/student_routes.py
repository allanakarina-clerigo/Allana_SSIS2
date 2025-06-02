from flask import render_template, url_for, redirect, request, flash, Blueprint
from ..models.student_models import Student
from flask_paginate import Pagination, get_page_args

students_bp = Blueprint('students', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Add these helper functions at the top of your route file
def get_pagination_args():
    page = request.args.get('page', 1, type=int)
    per_page = 10
    offset = (page - 1) * per_page
    return page, per_page, offset

def generate_pagination(page, per_page, total, keyword):
    # Calculate total pages
    if per_page == 0:
        total_pages = 1
    else:
        total_pages = (total + per_page - 1) // per_page
    
    # Create page range with gap indicators
    pages = []
    
    # Always show first page
    if page > 1:
        pages.append(1)
    
    # Show pages around current page
    start = max(2, page - 2)
    end = min(total_pages, page + 2)
    
    # Add gap indicator if needed
    if start > 2:
        pages.append(None)  # None represents gap
    
    # Add middle pages
    for p in range(start, end + 1):
        pages.append(p)
    
    # Add last page if needed
    if end < total_pages:
        if end < total_pages - 1:
            pages.append(None)  # Gap indicator
        pages.append(total_pages)
    
    return {
        'page': page,
        'per_page': per_page,
        'total': total,
        'pages': pages,
        'has_prev': page > 1,
        'prev_num': page - 1,
        'has_next': page < total_pages,
        'next_num': page + 1,
        'keyword': keyword
    }

# Then your Index route
@students_bp.route('/')
def Index():
    page, per_page, offset = get_pagination_args()
    keyword = request.args.get('tableSearch', '').strip()

    if keyword:
        students, total = Student.search(keyword, offset=offset, per_page=per_page)
        if total == 0:
            flash("No results found")
    else:
        total = Student.get_count()
        students = Student.get_paginated(offset=offset, per_page=per_page)

    courses = Student.get_courses()
    pagination = generate_pagination(page, per_page, total, keyword)
    
    return render_template(
        'index.html', 
        pagination=pagination,
        student_list=students, 
        course=courses
    )

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
    
    # Get pagination parameters
    page, per_page, offset = get_pagination_args()
    
    # Get search results with pagination
    search_results, total = Student.search(keyword, offset=offset, per_page=per_page)

    if search_results:
        # Create pagination object for search results
        pagination = Pagination(
            page=page, 
            per_page=per_page, 
            total=total,
            css_framework='bootstrap4'
        )
        
        courses = Student.get_courses()
        return render_template(
            'index.html', 
            student_list=search_results, 
            course=courses,
            pagination=pagination
        )
    else:
        flash("No results found")
        return redirect(url_for('students.Index'))