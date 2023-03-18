from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.students import Student
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from ..utils.decorators import admin_required
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity


student_namespace = Namespace('student', description='name space for student authentication')

signup_model = student_namespace.model(
    'Signup', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Full Name"),
        'mat_no' : fields.String(required=True, description= "A Matric Number"),
        'email' : fields.String(required=True, description= "An email"),
        'password' : fields.String(required=True, description= "A password"),
        
    }
)

user_model = student_namespace.model(
    'User', {
        'id' : fields.Integer(),
        'name' : fields.String(required=True, description= "Full Name"),
        'mat_no' : fields.String(required=True, description= "A Matric Number"),
        'email' : fields.String(required=True, description= "An email"),
        'password_hash' : fields.String(required=True, description= "A password"),     
    }
)

login_model = student_namespace.model(
    'Login', {
        'mat_no' : fields.String(required=True, description= "A Matric Number"),
        'password' : fields.String(required=True, description= "A password"),
        
    }
)

@student_namespace.route('/signup')
class SignUp(Resource):
    
    @admin_required()
    @student_namespace.expect(signup_model)
    @student_namespace.marshal_with(user_model)
    @student_namespace.doc(
        description= "Create a Student as Admin"
    )
    def post(self):
        """
            Sign up a Student as an Admin
        """
        data = request.get_json()
        
        new_user = Student(
            name = data.get('name'),
            mat_no = data.get('mat_no'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
        )
        new_user.save()
        return new_user, HTTPStatus.CREATED
    
    
@student_namespace.route("/login")
class Login(Resource):
    @student_namespace.expect(login_model)
    @student_namespace.doc(
        description= "Login a Student"
    )
    def post(self):
        """
            Login a Student & Get Tokens
        """
        data = request.get_json()
        mat_no = data.get("mat_no")
        password = data.get("password")
        user = Student.query.filter_by(mat_no=mat_no).first()
        
        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.mat_no)
            refresh_token = create_refresh_token(identity=user.mat_no)
            response = {
                'access_token' : access_token,
                'refresh_token' : refresh_token
            }
            return response, HTTPStatus.CREATED
        

@student_namespace.route("/refresh")
class Refresh(Resource):
    @jwt_required(refresh=True)
    @student_namespace.doc(
        description= "Student Refresh Access Token"
    )
    def post(self):
        """
            Refresh Student Access Token 
        """
        mat_no = get_jwt_identity()
        access_token = create_access_token(identity=mat_no)
        return {'access_token': access_token}, HTTPStatus.OK



@student_namespace.route("/student/<int:student_id>")
class GetUpdate(Resource):
    
    @student_namespace.expect(user_model)
    @student_namespace.marshal_with(user_model)
    @jwt_required()
    @student_namespace.doc(
        description= "Get a Student by ID"
    )
    def get(self, student_id):
        """
            Student can Fetch their Data by ID
        """
        mat_no = get_jwt_identity()
        student_mat_no = Student.query.filter_by(mat_no=mat_no).first()
        if (student_mat_no.id != student_id):
           return "You are not Authorised to perform this action", HTTPStatus.BAD_REQUEST
        else:
            student = Student.get_by_id(student_id)
            return student, HTTPStatus.OK
    
    @jwt_required()
    @student_namespace.doc(
        description= "Student Data by ID"
    )
    @student_namespace.expect(user_model)
    @student_namespace.marshal_with(user_model)
    def put(self, student_id):
        """
            Edit a Student by Id
        """
        mat_no = get_jwt_identity()
        student_mat_no = Student.query.filter_by(mat_no=mat_no).first()
        if (student_mat_no.id != student_id):
           return "You are not Authorised to perform this action", HTTPStatus.BAD_REQUEST
        else:
            student = Student.get_by_id(student_id)
            print("This is the Student: ", student)
            data = student_namespace.payload
            student.name = data['name']
            student.email = data['email']
            student.password_hash = generate_password_hash(data['password'])
            student.edit()
            return student, HTTPStatus.ACCEPTED
    
 