from flask_restx import Namespace, Resource, fields
from ..models.admin import Admin
from ..utils.decorators import admin_required
from werkzeug.security import generate_password_hash
from http import HTTPStatus
from flask_jwt_extended import get_jwt_identity

admin_namespace = Namespace('admin', description='Namespace for Administrators')

admin_signup_model = admin_namespace.model(
    'AdminSignup', {
        'username': fields.String(required=True, description="Username"),
        'name': fields.String(required=True, description="Admin's Full Name"),
        'email': fields.String(required=True, description="Admin's Email"),
        'password': fields.String(required=True, description="Admin's Password")
    }
)

admin_model = admin_namespace.model(
    'Admin', {
        'id': fields.Integer(description="Admin's User ID"),
        'username': fields.String(required=True, description="Username"),
        'name': fields.String(required=True, description="Admin's Email"),
        'email': fields.String(required=True, description="Admin's Email"),
        'user_type': fields.String(required=True, description="Type of User")
    }
)

@admin_namespace.route('/admins')
class GetAllAdmins(Resource):

    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description="Retrieve All Admins as an Admin"
    )
    @admin_required()
    def get(self):
        """
            Retrieve All Admins as an Admin
        """
        admins = Admin.query.all()

        return admins, HTTPStatus.OK

@admin_namespace.route('/register')
class AdminRegistration(Resource):

    @admin_namespace.expect(admin_signup_model)
    # Uncomment the @admin_required() decorator below after registering the first admin
    # This ensures that only an existing admin can register a new admin account on the app
    # @admin_required()
    @admin_namespace.doc(
        description = "Register Admin"
    )
    def post(self):
        """
            Register  Admin
        """        
        data = admin_namespace.payload

        # Check if the admin account already exists
        admin = Admin.query.filter_by(email=data['email']).first()
        if admin:
            return {"message": "Admin Account Already Exists"}, HTTPStatus.CONFLICT

        # Register new admin
        new_admin = Admin(
            username = data['username'],
            name = data['name'],
            email = data['email'],
            password_hash = generate_password_hash(data['password']),
            user_type = 'admin'
        )

        new_admin.save()

        admin_resp = {}
        admin_resp['id'] = new_admin.id
        admin_resp['username'] = new_admin.username
        admin_resp['name'] = new_admin.name
        admin_resp['email'] = new_admin.email
        admin_resp['user_type'] = new_admin.user_type

        return admin_resp, HTTPStatus.CREATED

@admin_namespace.route('/<int:admin_id>')
class GetUpdateDeleteAdmins(Resource):
    
    @admin_namespace.marshal_with(admin_model)
    @admin_namespace.doc(
        description = "Retrieve an Admin's Details by ID as an Admin"
    )
    @admin_required()
    def get(self, admin_id):
        """
            Retrieve an Admin's Details by ID as an Admin
        """
        admin = Admin.get_by_id(admin_id)
        
        return admin, HTTPStatus.OK
    
    @admin_namespace.expect(admin_signup_model)
    @admin_namespace.doc(
        description = "Update an Admin's Details by ID as an Admin"
    )
    @admin_required()
    def put(self, admin_id):
        """
            Update an Admin's Details by ID as an Admin
        """
        admin = Admin.get_by_id(admin_id)
        active_admin = get_jwt_identity()
        
        if active_admin != admin.username:
            return {"message": "For a Specific Admin Only"}, HTTPStatus.FORBIDDEN

        data = admin_namespace.payload

        admin.username = data['username']
        admin.name = data['name']
        admin.email = data['email']
        admin.password_hash = generate_password_hash(data['password'])

        admin.update()

        admin_resp = {}
        admin_resp['id'] = admin.id
        admin_resp['username'] = admin.username
        admin_resp['name'] = admin.name
        admin_resp['email'] = admin.email
        admin_resp['user_type'] = admin.user_type

        return admin_resp, HTTPStatus.OK
    
    @admin_namespace.doc(
        description = "Delete an Admin by ID as an Admin"
    )
    @admin_required()
    def delete(self, admin_id):
        """
            Delete an Admin by ID as an Admin
        """
        admin = Admin.get_by_id(admin_id)

        admin.delete()

        return {"message": "Admin has been Successfully Deleted"}, HTTPStatus.OK