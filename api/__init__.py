from flask import Flask 
from flask_restx import Api
from .utils.blacklist import BLACKLIST
from .courses.views import course_namespace
from .students.views import student_namespace
from .teachers.views import teacher_namespace
from .grades.views import grade_namespace
from .admin.views import admin_namespace
from .config.config import config_dict
from .utils import db
from .models.courses import Course
from .models.students import Student
from .models.teachers import Teacher
from .models.grades import Grade
from .models.admin import Admin
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed



def create_app(config=config_dict['dev']):
    app = Flask(__name__)
    
    app.config.from_object(config)
    
    db.init_app(app)
    
    jwt = JWTManager(app)
    
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blacklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLACKLIST
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has been revoked",
            "error": "token_revoked"
        }
    
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        return {
            "message": "The token has expired",
            "error": "token_expired"
        }
    
    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        return {
            "message": "Token verification failed",
            "error": "invalid_token"
        }
    
    @jwt.unauthorized_loader
    def missing_token_callback(error):
        return {
            "message": "Request is missing an access token",
            "error": "authorization_required"
        }
    
    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {
            "message": "The token is not fresh",
            "error": "fresh_token_required"
        }
    
    migrate = Migrate(app, db)
    
    authorizations={
        "Bearer Auth": {
            'type': "apiKey",
            'in': 'header',
            'name': "Authorization",
            'description': "Add a JWT with ** Bearer &lt;JWT&gt; to authorize"
        }
    }
    
    api = Api(app,
              title="School API",
              description="A REST API for a School for Teachers to grade and register students. ",
              authorizations=authorizations,
              security="Bearer Auth"
            )
    
    api.add_namespace(course_namespace, path='/courses')
    api.add_namespace(student_namespace, path='/students')
    api.add_namespace(teacher_namespace, path='/teachers')
    api.add_namespace(admin_namespace, path='/admin')
    api.add_namespace(grade_namespace, path='/grades')
    
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db' : db,
            'Student' : Student,
            'Course' : Course,
            'Teacher' : Teacher,
            'Grade' : Grade,
            'Admin' : Admin
        }
    
    return app