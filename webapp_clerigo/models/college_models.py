from .database import DatabaseManager

class College:
    @staticmethod
    def get_all():
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM college_list")
        data = cursor.fetchall()
        cursor.close()
        conn.close()
        return data

    @staticmethod
    def create(college_code, college_name):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO college_list (college_code, college_name) VALUES (%s, %s)",
            (college_code, college_name)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def update(college_code, college_name):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE college_list SET college_name=%s WHERE college_code=%s",
            (college_name, college_code)
        )
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def delete(college_code):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM college_list WHERE college_code=%s", (college_code,))
        conn.commit()
        cursor.close()
        conn.close()

    @staticmethod
    def search(keyword):
        conn = DatabaseManager.get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM college_list")
        colleges = cursor.fetchall()
        cursor.close()
        conn.close()
        
        result = []
        for college in colleges:
            college_allcaps = [str(info).upper() for info in college.values()]
            if keyword in college_allcaps:
                result.append(college)
        return result