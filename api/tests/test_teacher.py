import unittest
from .. import create_app
from ..config.config import config_dict
from ..utils import db
from ..models.teachers import Teacher
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
    
    def test_teacher_registration(self):
        
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
            "name" : "john deep",
            "username" : "testteacher",
            "email" : "testteacher@gmail.com",
            "password" : "passwword"
        }
             
        response=self.client.post('teachers/signup', json=data, headers=headers)
        
        assert response.status_code == 201
        
        teacher=Teacher.query.filter_by(email="testteacher@gmail.com").first()
        
        assert teacher.username == "testteacher"
                
    def test_login(self) :
        
        data={
            "username": "testteacher",
            "password": "12345"
        }
            
           
        response=self.client.post('teachers/login', json=data)
        
        assert response.status_code == 200
        