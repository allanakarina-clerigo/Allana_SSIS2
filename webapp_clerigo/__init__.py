from flask import Flask
from flask_mysqldb import MySQL
from webapp_clerigo.configure import SECRET_KEY, DB_HOST, DB_USER, DB_PASSWORD, DB_DATABASE, DB_PORT, CLOUD_NAME, API_KEY, API_SECRET
from os import getenv
import cloudinary
mysql = MySQL()


cloudinary.config(
            cloud_name = CLOUD_NAME,
            api_key = API_KEY,
            api_secret = API_SECRET)

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = SECRET_KEY
    app.config['MYSQL_HOST'] = DB_HOST
    app.config['MYSQL_PORT'] = DB_PORT
    app.config['MYSQL_USER'] = DB_USER
    app.config['MYSQL_PASSWORD'] = DB_PASSWORD
    app.config['MYSQL_DB'] = DB_DATABASE

    mysql.init_app(app)
    # import blueprints
    
    from .routes.student_routes import students_bp
    from .routes.college_routes import colleges_bp
    from .routes.course_routes import courses_bp


    # register blueprints
    app.register_blueprint(students_bp, url_prefix='/')
    app.register_blueprint(courses_bp, url_prefix='/')
    app.register_blueprint(colleges_bp, url_prefix='/')

    return app