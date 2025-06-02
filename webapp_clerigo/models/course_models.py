from .database import DatabaseManager

class Course:
    @staticmethod
    def get_all():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course_list")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def get_colleges():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM college_list")
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        return colleges

    @staticmethod
    def create(course_code, course_name, college):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO course_list (course_code, course_name, college) VALUES (%s, %s, %s)",
            (course_code, course_name, college)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(course_code, course_name, college):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE course_list SET course_name=%s, college=%s WHERE course_code=%s",
            (course_name, college, course_code)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(course_code):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM course_list WHERE course_code=%s", (course_code,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM course_list")
        courses = cursor.fetchall()
        cursor.close()
        conn.close()
        
        result = []
        for course in courses:
            course_allcaps = [str(info).upper() for info in course.values()]
            if keyword in course_allcaps:
                result.append(course)
        return result