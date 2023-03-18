import unittest
from .. import create_app
from ..config.config import config_dict
from ..models.courses import Course
from ..models.teachers import Teacher
from ..models.admin import Admin
from..utils import db
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token

class CourseTestCase(unittest.TestCase):
    def setUp(self):
        self.app=create_app(config=config_dict['test'])
        self.appctx=self.app.app_context()
        
        self.appctx.push()
        
        self.client=self.app.test_client()
        
        db.create_all()
        
    def tearDown(self):
        db.drop_all()
        
        self.app=None
        
        self.appctx.pop()
        
        self.client=None
        
    def test_get_all_courses(self):
        
        admin_signup_data = {
            "username": "Test",
            "name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.username)

        headers1 = {
            "Authorization": f"Bearer {token}"
        }
        
        # Activate a test teacher
        teacher_signup_data = {
            "name": "TesterTested",
            "username": "HODTest",
            "email": "hodtest@gmail.com",
            "password": "password"
        }
             
        response=self.client.post('/teachers/signup', json=teacher_signup_data, headers=headers1)
        
        print("This is the response status code: ", response.status_code)
        print("This is the response data: ", response.get_json())

        teacher = Teacher.query.filter_by(email='hodtest@gmail.com').first()

        token = create_access_token(identity=teacher.username)
        
        headers={
            "Authorization": f"Bearer {token}"
        }
        
        response=self.client.get('/courses/courses', headers=headers)
        
        assert response.status_code == 200
        
    def test_create_course(self):
        
        admin_signup_data = {
            "username": "Test",
            "name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.username)

        headers1 = {
            "Authorization": f"Bearer {token}"
        }
        
        teacher_signup_data = {
            "name": "Tester Tested",
            "username": "HODTest",
            "email": "hodtest@gmail.com",
            "password": "password"
        }
        response = self.client.post('/teachers/signup', json=teacher_signup_data, headers=headers1)

        print("This is the response status code: ", response.status_code)
        print("This is the response data: ", response.get_json())

        
        teacher = Teacher.query.filter_by(email='hodtest@gmail.com').first()
        
        print("This is the teacher: ", teacher)
        

        token = create_access_token(identity=teacher.username)
        
        print("This is the token: ", token)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        data={
            "id": 0,
            "name": "string",
            "course_unit": 0,
            "teacher_name": "string",
            "students": [],
            "teacher_id": 0
        }   
        
        print("This is the header: ", headers)
        
        
        response=self.client.post('/courses/courses', json=data, headers=headers)
        
        print("This is the response status code: ", response.status_code)
        print("This is the response data: ", response.get_json())
        
        assert response.status_code == 201
        
        courses = Course.query.all()
        
        assert len(courses) == 1    
                    