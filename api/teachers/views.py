from flask import request
from flask_restx import Namespace, Resource, fields
from ..utils.decorators import admin_required, get_user_type
from ..models.teachers import Teacher
from ..models.students import Student
from ..utils.blacklist import BLACKLIST
from ..utils import db
from ..models.courses import Course
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt

teacher_namespace = Namespace('teachers', description='name space for authentication for admins and teacher')

signup_model = teacher_namespace.model(
    'Signup', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Teacher's Name"),
        'username' : fields.String(required=True, description= "A username"),
        'email' : fields.String(required=True, description= "An email"),
        'password' : fields.String(required=True, description= "A password"),
        
    }
)

newstudent_model = teacher_namespace.model(
    'Signup', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Full Name"),
        'mat_no' : fields.String(required=True, description= "A Matric Number"),
        'email' : fields.String(required=True, description= "An email"),
        'password' : fields.String(required=True, description= "A password"),
        
    }
)

student_model = teacher_namespace.model(
    'Student', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Full Name"),
        'mat_no' : fields.String(required=True, description= "A Matric Number"),
        'email' : fields.String(required=True, description= "An email"),
        'password_hash' : fields.String(required=True, description= "A password"),     
    }
)

user_model = teacher_namespace.model(
    'User', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Full Name"),
        'username' : fields.String(required=True, description= "A username"),
        'email' : fields.String(required=True, description= "An email"),
        'password_hash' : fields.String(required=True, description= "A password"),
        'user_type': fields.String(required=True, description="Type of User")
       
    }
)

login_model = teacher_namespace.model(
    'Login', {
        'username' : fields.String(required=True, description= "A username"),
        'password' : fields.String(required=True, description= "A password"),
        
    }
)

def is_teacher_or_admin(username:str) -> bool:
    claims = get_jwt()
    active_user_id = get_jwt_identity()
    if (get_user_type(claims['sub']) == 'admin') or (active_username == student_id):
        return True
    else:
        return False

#Teacher Login/Signup endpoints
@teacher_namespace.route('/signup')
class SignUp(Resource):
    
    @teacher_namespace.expect(signup_model)
    @teacher_namespace.marshal_with(user_model)
    @teacher_namespace.doc(
        description= "Create a teacher as Admin",
        params={
            "name" : "Pass in the Teachers name Here",
            "username" : "Give the Teacher a Username",
            "email" : "Add the Email of the Lecturer",
            "password" : "Create a Password for the Teacher"
        }
    )
    @admin_required()
    def post(self):
        """
            Sign up a Teacher
        """
        data = request.get_json()
        new_user = Teacher(
            name = data.get('name'),
            username = data.get('username'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password')),
            user_type = 'teacher'
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED
    
    
@teacher_namespace.route("/login")
class Login(Resource):
    @teacher_namespace.expect(login_model)
    @teacher_namespace.doc(
        description= "Login a Teacher/Admin"
    )
    def post(self):
        """
            Login a Teacher/Admin & Get Tokens
        """
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'Invalid login credentials' 
       
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)
            response = {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
            return response, HTTPStatus.CREATED
        
        

@teacher_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @teacher_namespace.doc(
        description= "Refresh Teacher/Admin Token"
    )
    def post(self):
        """
            Refresh User Access Token 
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        access_token = create_access_token(identity=username)
        
        if (user is None):
           return {'Invalid': 'Token credentials'}
        else:
            return {'access_token': access_token, 'username' : username}, HTTPStatus.OK

@teacher_namespace.route("/teacher")
class GetTeacher(Resource):
    
    @teacher_namespace.marshal_with(user_model)
    @teacher_namespace.doc(
        description= "Get all Teachers"
    )
    @admin_required()
    def get(self):
        """
            Get all Teachers 
        """
        teacher = Teacher.query.filter(Teacher.user_type == "teacher").all()
        print("This is the teacher : ", teacher)
        return teacher, HTTPStatus.OK


@teacher_namespace.route("/teacher/<int:teacher_id>")
class GetUpdateDeleteTeacher(Resource):
    
    @teacher_namespace.expect(user_model)
    @teacher_namespace.marshal_with(user_model)
    @teacher_namespace.doc(
        description= "Get Teacher by ID"
    )
    @admin_required()
    def get(self, teacher_id):
        """
            Get Teachers by ID
        """
        teacher = Teacher.query.filter(Teacher.id==teacher_id, Teacher.user_type == "teacher").first()
        if teacher:
            return teacher, HTTPStatus.OK
        else :
            return {"error " : " Teacher not Found"}, HTTPStatus.NOT_FOUND
    
    @admin_required()
    @teacher_namespace.doc(
        description= "Edit a Teacher by ID"
    )
    @teacher_namespace.expect(signup_model)
    @teacher_namespace.marshal_with(user_model)
    def put(self, teacher_id):
        """
            Edit a Teacher by Id
        """
        teacher = Teacher.query.filter(Teacher.id==teacher_id, Teacher.user_type == "teacher").first()
        if teacher:
            teacher = Teacher.get_by_id(teacher_id)
            data = teacher_namespace.payload
            teacher.name = data['name']
            teacher.username = data['username']
            teacher.email = data['email']
            teacher.password_hash = generate_password_hash(data['password'])
            teacher.edit()
            return teacher, HTTPStatus.ACCEPTED
        else:
            return {"error " : " Teacher not Found"}, HTTPStatus.NOT_FOUND
    
    @teacher_namespace.doc(
        description= "Delete a Teacher by ID"
    )
    @admin_required()
    def delete(self, teacher_id):
        """
            Delete a Teacher by ID as Admin
        """
        teacher = Teacher.query.filter(Teacher.id==teacher_id, Teacher.user_type == "teacher").first()
        if teacher:
            teacher_to_delete = Teacher.get_by_id(teacher_id)
            teacher_to_delete.delete()
            return {"message": "Deleted Successfully"}, HTTPStatus.OK
        else:
            return {"error " : " Teacher not Found"}, HTTPStatus.NOT_FOUND

#Student
@teacher_namespace.route("/students")
class StudentGetCreate(Resource):
    @teacher_namespace.marshal_with(student_model)
    @teacher_namespace.doc(
        description= "Get all Students"
    )
    @jwt_required()
    def get(self):
        """
            Get all Students 
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            students = Student.query.all()
            return students, HTTPStatus.OK
    
    @teacher_namespace.expect(newstudent_model)
    @teacher_namespace.marshal_with(student_model)
    @teacher_namespace.doc(
        description= "Create a Student"
    )
    @admin_required()
    def post(self):
        """
            Create a Student as an Admin 
        """
        username = get_jwt_identity()
        current_user = Teacher.query.filter_by(id=username).first()
        data = request.get_json()
        new_student = Student(
            name = data.get('name'),
            mat_no = data.get('mat_no'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        new_student.teacher_id = current_user
        new_student.save()
        return new_student, HTTPStatus.CREATED

@teacher_namespace.route("/student/<int:student_id>")
class GetUpdateDelete(Resource):
    
    @teacher_namespace.expect(newstudent_model)
    @teacher_namespace.marshal_with(newstudent_model)
    @jwt_required()
    @teacher_namespace.doc(
        description= "Get a Student by ID"
    )
    def get(self, student_id):
        """
            Get a student by ID
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            student = Student.get_by_id(student_id)
            return student, HTTPStatus.OK
    
    
    @admin_required()
    @teacher_namespace.doc(
        description= "Edit a Student by ID"
    )
    @teacher_namespace.expect(newstudent_model)
    @teacher_namespace.marshal_with(newstudent_model)
    def put(self, student_id):
        """
            Edit a Student by Id
        """
        student = Student.get_by_id(student_id)
        data = teacher_namespace.payload
        student.name = data['name']
        student.mat_no = data['mat_no']
        student.email = data['email']
        student.password_hash = generate_password_hash(data['password'])
        student.edit()
        return student, HTTPStatus.ACCEPTED
    
    @teacher_namespace.doc(
        description= "Delete a Student by ID"
    )
    @teacher_namespace.marshal_with(student_model)
    @admin_required()
    def delete(self, student_id):
        """
            Delete a Student by ID as Admin
        """
        student_to_delete = Student.get_by_id(student_id)
        student_to_delete.delete()
        return {"message": "Deleted Successfully"}, HTTPStatus.OK
    
    
@teacher_namespace.route('/logout')
class Logout(Resource):
    @jwt_required(verify_type=False)
    def post(self):
        """
            Revoke Access/Refresh Token
        """
        token = get_jwt()
        jti = token["jti"]
        token_type = token["type"]
        BLACKLIST.add(jti)
        return {"message": f"{token_type.capitalize()} token successfully revoked"}, HTTPStatus.OK

    
