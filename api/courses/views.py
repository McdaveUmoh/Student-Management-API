from flask_restx import Namespace, Resource, fields, reqparse
from ..models.courses import Course
from ..utils import db
from ..models.teachers import Teacher
from ..models.students import Student
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity
 

course_namespace = Namespace('courses', description='name space for Course')

# Course model for registering courses and retrieving grades
course_model = course_namespace.model(
    'Course',{
        'id': fields.Integer(description="An ID"),
        'name': fields.String(description="Course Name", required=True),
        'course_unit': fields.Integer(description="Course Unit", required=True),
        'teacher_name': fields.String(description="Course Teacher", required=True),
        'students': fields.List(fields.Integer),
        'teacher_id': fields.Integer(description="Teacher ID")
    }
)
courseslist = course_namespace.model(
    'CoursesList',{
        'id': fields.Integer(description="An ID"),
        'name': fields.String(description="Course Name", required=True),
        'course_unit': fields.Integer(description="Course Unit", required=True),
        'teacher_id': fields.Integer(description="Teacher ID"),
        'teacher_name': fields.String(description="Course Teacher", required=True),
        
    }
)

@course_namespace.route("/courses")
class CourseGetCreate(Resource):
    @course_namespace.marshal_with(courseslist)
    @course_namespace.doc(
        description= "Get all Courses"
    )
    # @jwt_required()
    def get(self):
        """
            Get all Courses
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return {"Error":"You are not Authorised to perform this action"} , HTTPStatus.FORBIDDEN
        else:
            courses = Course.query.all()
            return courses, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description= "Create a course as a teacher"
    )
    @jwt_required()
    def post(self):
        """
            create a course as a teacher 
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            username = get_jwt_identity()
            current_teacher = Teacher.query.filter_by(username=username).first()
            data = course_namespace.payload
            course = Course(
                name =  data['name'],
                course_unit =  data['course_unit'],
                teacher_name = data['teacher_name'],
                students = data['students']
            )
            
            for student_id in data['students']:
                
                # Filter the Student table by ID
                student = Student.query.filter_by(id=student_id).first()
                
                # If the student exists, append it to the course's students list
                if student and student not in course.students:
                    course.students.append(student_id)
                else:
                    return 'error', HTTPStatus.FORBIDDEN
                
            # define the parser to accept a list of integers
            parser = reqparse.RequestParser()
            parser.add_argument('students', type=int, action='append')

            # get the list of integers from the request
            data = parser.parse_args()

            # remove duplicates using a set
            unique_students = list(set(course.students))
            course.students = unique_students
            course.teacher_id = current_teacher.id
            course.save()
            return course, HTTPStatus.CREATED
            
            
    
@course_namespace.route("/course/<int:course_id>")
class GetUpdateDelete(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description= "Get a Specific Course by ID"
    )
    @jwt_required()
    def get(self, course_id):
        """
            Get a course by ID as teacher
        """
        course = Course.get_by_id(course_id)
        return course, HTTPStatus.OK
    
    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description= "Edit a Course by ID"
    )
    @jwt_required()
    def put(self, course_id):
        """
            Put  Course by ID
        """
        username = get_jwt_identity()
        current_teacher = Teacher.query.filter_by(username=username).first()
        course_to_update = Course.get_by_id(course_id)
        data = course_namespace.payload
        course_to_update.name = data["name"]
        course_to_update.course_unit = data["course_unit"]
        course_to_update.teacher_name = data["teacher_name"]
        
        
        for student_id in data['students']:
                # Filter the Student table by ID
                student = Student.query.filter_by(id=student_id).first()
                #existing_student = course.students[student_id]
                # If the student exists, append it to the course's students list
                if student and student not in course_to_update.students:
                    course_to_update.students.append(student_id)
                else:
                    return 'error', HTTPStatus.FORBIDDEN
                
        # define the parser to accept a list of integers
        parser = reqparse.RequestParser()
        parser.add_argument('students', type=int, action='append')
        # get the list of integers from the request
        data = parser.parse_args()

        # remove duplicates using a set
        unique_students1 = list(set(course_to_update.students))
        course_to_update.students = unique_students1
        course_to_update.teacher_id = current_teacher.id
        

        db.session.commit()

        return course_to_update, HTTPStatus.OK
    
    @course_namespace.doc(
        description= "Delete a Course by ID"
    )
    @jwt_required()
    def delete(self, course_id):
        """
            Delete a course by ID
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            course_to_delete = Course.get_by_id(course_id)
            course_to_delete.delete()
            return {"message": "Deleted Successfully"}, HTTPStatus.OK
    
@course_namespace.route('/courselist')
class AllCourses(Resource):
    
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description= "Get all Courses with Enrolled Students"
    )
    @jwt_required()
    def get(self):
        """
            Get all Courses with enrolled students
        """
        course = Course.query.all()
        return course, HTTPStatus.OK
        

@course_namespace.route('/teacher/<int:teacher_id>/courses')
class GetTeacherCourses(Resource):
    
    #use marshal_list_with when returning a bunch of list as opposed to marshal_with
    @course_namespace.marshal_list_with(course_model)
    @course_namespace.doc(
        description= "Get all Courses of a Teacher by ID"
    )
    @jwt_required()
    def get(self, teacher_id):
        """
            Get all teacher Courses
        """
        teacher = Teacher.get_by_id(teacher_id)
        courses = teacher.courses
        return courses, HTTPStatus.OK
