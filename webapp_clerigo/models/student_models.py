from .database import DatabaseManager
from cloudinary.uploader import upload, destroy

class Student:
    @staticmethod
    def get_all():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_list")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def get_courses():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course_list")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        return courses

    @staticmethod
    def create(stud_id, url, fname, lname, year_lvl, gender, course):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO student_list 
            (stud_id, photo_link, fname, lname, year_lvl, gender, course_code) 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (stud_id, url, fname, lname, year_lvl, gender, course))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_with_photo(url, fname, lname, year_lvl, gender, course, stud_id):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE student_list 
            SET photo_link=%s, fname=%s, lname=%s, 
                year_lvl=%s, gender=%s, course_code=%s 
            WHERE stud_id=%s
        """, (url, fname, lname, year_lvl, gender, course, stud_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update_without_photo(fname, lname, year_lvl, gender, course, stud_id):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE student_list 
            SET fname=%s, lname=%s, year_lvl=%s, 
                gender=%s, course_code=%s 
            WHERE stud_id=%s
        """, (fname, lname, year_lvl, gender, course, stud_id))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(stud_id):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student_list WHERE stud_id=%s", (stud_id,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_list")
        students = cursor.fetchall()
        cursor.close()
        conn.close()
        
        result = []
        for student in students:    
            student_allcaps = [str(info).upper() for info in student.values()]
            if keyword in student_allcaps:
                result.append(student)
        return result

    @staticmethod
    def upload_photo(file, stud_id):
        return upload(file.read(), public_id=f"ssis/{stud_id}")['url']

    @staticmethod
    def delete_photo(stud_id):
        destroy(public_id=f"ssis/{stud_id}")
