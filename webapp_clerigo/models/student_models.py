from .database import DatabaseManager
from cloudinary.uploader import upload, destroy
import re

class Student:
    @staticmethod
    def get_count():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT COUNT(*) as total FROM student_list")
        result = cursor.fetchone()
        total = result['total']
        cursor.close()
        conn.close()
        return total

    @staticmethod
    def get_paginated(offset=0, per_page=10):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM student_list LIMIT %s OFFSET %s", (per_page, offset))
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
        if not re.match(r'^\d{4}-\d{4}$', stud_id):
            raise ValueError("Student ID must be in format XXXX-XXXX")
            
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
    def search(keyword, offset=0, per_page=10):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        
        # SQL-based search
        pattern = f'%{keyword}%'
        query = """
            SELECT SQL_CALC_FOUND_ROWS * 
            FROM student_list 
            WHERE 
                UPPER(stud_id) LIKE UPPER(%s) OR
                UPPER(fname) LIKE UPPER(%s) OR
                UPPER(lname) LIKE UPPER(%s) OR
                UPPER(course_code) LIKE UPPER(%s) OR
                UPPER(year_lvl) LIKE UPPER(%s) OR
                UPPER(gender) LIKE UPPER(%s)
            LIMIT %s OFFSET %s
        """
        cursor.execute(query, (pattern, pattern, pattern, pattern, pattern, pattern, per_page, offset))
        results = cursor.fetchall()
        
        # Get total count
        cursor.execute("SELECT FOUND_ROWS() as total")
        total = cursor.fetchone()['total']
        
        cursor.close()
        conn.close()
        return results, total

    @staticmethod
    def upload_photo(file, stud_id):
        return upload(file.read(), public_id=f"ssis/{stud_id}")['url']

    @staticmethod
    def delete_photo(stud_id):
        destroy(public_id=f"ssis/{stud_id}")

    @staticmethod
    def upload_photo(file, stud_id):
        MAX_SIZE = 2 * 1024 * 1024  # 2MB

        # Check file size
        file.seek(0, 2)  # Move to end of file
        file_size = file.tell()
        file.seek(0)  # Reset file pointer
        
        if file_size > MAX_SIZE:
            raise ValueError("File size exceeds 2MB limit")
        
        # Check file signature
        header = file.read(8)
        file.seek(0)  # Reset for Cloudinary upload
        
        # PNG signature (first 8 bytes)
        png_sig = b'\x89PNG\r\n\x1a\n'
        # JPEG signature (first 2 bytes)
        jpg_sig = b'\xFF\xD8'
        
        if not header.startswith(png_sig) and not (header[:2] == jpg_sig):
            raise ValueError("Invalid file format. Only PNG and JPG are allowed")
        
        return upload(file.read(), public_id=f"ssis/{stud_id}")['url']