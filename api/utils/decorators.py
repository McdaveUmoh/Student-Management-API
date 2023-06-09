from ..models.teachers import Teacher
from flask_jwt_extended import get_jwt, verify_jwt_in_request
from functools import wraps
from http import HTTPStatus

# Get the user type for use in the @admin_required() decorator
def get_user_type(username:str):
    user = Teacher.query.filter_by(username=username).first()
    if user:
        return user.user_type
    else:
        return None

# Custom decorator to verify admin access
def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            if get_user_type(claims['sub']) == 'admin':
                return fn(*args, **kwargs)
            else:
                return {"message": "Administrator access required"}, HTTPStatus.FORBIDDEN
        return decorator
    return wrapper