from os import getenv
import mysql.connector
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager: 
    """Handles all database connections"""  
    @staticmethod
    def get_db_connection():
        """Establish a connection to MySQL database."""
        conn = mysql.connector.connect(
            host=getenv('DB_HOST'),
            user=getenv('DB_USERNAME'),
            password=getenv('DB_PASSWORD'),
            database=getenv('DB_NAME'),
            auth_plugin='mysql_native_password'
        )
        return conn