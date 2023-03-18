import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.students import Student
from ..models.admin import Admin
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token


class UserTestCase(unittest.TestCase) :
    def setUp(self):
        self.app=create_app(config=config_dict['test'])
        
        self.appctx = self.app.app_context()
        
        self.appctx.push()
        
        self.client=self.app.test_client()
        
        db.create_all()
        
    def tearDown(self) :
        db.drop_all()
        
        self.appctx.pop()
        
        self.app=None
        
        self.client=None
    
    def test_student_registration(self):
        
        admin_signup_data = {
            "username": "Test",
            "name": "Admin",
            "email": "testadmin@gmail.com",
            "password": "password"
        }

        response = self.client.post('/admin/register', json=admin_signup_data)

        admin = Admin.query.filter_by(email='testadmin@gmail.com').first()

        token = create_access_token(identity=admin.username)

        headers = {
            "Authorization": f"Bearer {token}"
        }
        
        
        data={
            "name": "testuser",
            "mat_no": "com/419",
            "email": "testuser@gmail.com",
            "password": "password"
        }
             
        response=self.client.post('students/signup', json=data, headers=headers)
        
        student=Student.query.filter_by(mat_no="com/419").first()
        
        assert student.name == "testuser"
        
        assert response.status_code == 201
        
    def test_login(self) :
        
        data={
            "mat_no": "com/419",
            "password": "password"
        }
            
           
        response=self.client.post('students/login', json=data)
        
        assert response.status_code == 200
        