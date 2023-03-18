from flask_restx import Namespace, Resource, fields, reqparse
from ..models.courses import Course
from ..utils import db
from ..models.teachers import Teacher
from ..models.students import Student
from ..models.grades import Grade
from sqlalchemy.exc import IntegrityError
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity


grade_namespace = Namespace('grades', description='name space for Grade')

# Grade Model for CRUD students grade
grade_model = grade_namespace.model(
    'Grade',{
        'id': fields.Integer(description="An ID"),
        'grade': fields.Float(description="Course Grade", required=True),
        'student_id': fields.Integer(description="Course Unit"),
        'course_id': fields.Integer(description="Course Teacher"),
        'teacher_id': fields.Integer(description="Teacher ID")
    }
)

def calculate_gpa(grades):
    total_gpa = 0.0
    for grade in grades:
        if grade >= 90:
            total_gpa += 4.0
        elif grade >= 80:
            total_gpa += 3.0
        elif grade >= 70:
            total_gpa += 2.0
        elif grade >= 60:
            total_gpa += 1.0
    if len(grades) > 0:
        gpa = total_gpa / len(grades)
        return round(gpa, 2)
    return 0.0 
 

@grade_namespace.route("/grade-student/<int:course_id>/<int:student_id>")
class GradeStudent(Resource):
    
    @grade_namespace.expect(grade_model)
    @grade_namespace.marshal_with(grade_model)
    @jwt_required()
    @grade_namespace.doc(
        description= " Create a Grade for a Student as a Teacher"
    )
    def post(self, course_id, student_id):
        """
            create a Grade for a Student as a Teacher 
        """
        student = Student.get_by_id(student_id)
        course = Course.get_by_id(course_id)
        coursegradelist = Grade.query.filter_by(course_id=course_id).first()
        studentgradelist = Grade.query.filter_by(student_id=student_id).first()
        username = get_jwt_identity()
        
        
        teacher = Teacher.query.filter_by(username=username).first()
        if (teacher is None):
           return {'You are not Authorised to perform this action'}, HTTPStatus.FORBIDDEN
        else:
            if student.id in course.students :
                
                data = grade_namespace.payload
                
                grade = Grade(
                    grade=data['grade']
                )
                grade.course_id = course.id
                grade.teacher_id = teacher.id
                grade.student_id = student.id
                if studentgradelist and studentgradelist.course_id == course_id:
                    return {'error' : 'error student already graded'}, HTTPStatus.BAD_REQUEST
                elif Grade.query.filter_by(student_id=student_id, course_id=course_id).first():
                    return {'error': 'error student already has grade for this course'}, HTTPStatus.BAD_REQUEST
                else:
                    grade.save()
                    return grade, HTTPStatus.CREATED
            else:
                return {'This student is not enrolled in this course'}, HTTPStatus.BAD_REQUEST


@grade_namespace.route("/grade/<int:grade_id>")
class GetDelete(Resource):
    
    @grade_namespace.marshal_with(grade_model)
    @jwt_required()
    @grade_namespace.doc(
        description= " Get a Grade as a Teacher"
    )
    def get(self, grade_id):
        """
            Get a grade by Id as teacher
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return {"Error": "You are not Authorised to perform this action"}, HTTPStatus.FORBIDDEN
        else:
            grade = Grade.get_by_id(grade_id)
            return grade, HTTPStatus.OK
    
    
    @jwt_required()
    @grade_namespace.doc(
        description= " Delete a Grade as a Teacher"
    )
    def delete(self, grade_id):
        """
            Delete a Grade by Id as teacher
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            grade_to_delete = Grade.get_by_id(grade_id)
            grade_to_delete.delete()
            return {"message": "Deleted Successfully"}, HTTPStatus.OK

@grade_namespace.route("/grade/<int:student_id>/gpa")
class StudentGPA(Resource): 
    
    @jwt_required()
    @grade_namespace.doc(
        description= " Get a Particular Student GPA"
    )
    def get(self, student_id):
        """
            View Student Grade by ID as Teacher or Student
        """
        username = get_jwt_identity()
        student = Student.get_by_id(student_id)
        user = Teacher.query.filter_by(username=username).first()
        
        if user :
            grades_list = []
            GradeList = Grade.query.all()
            for grade in GradeList:
                if grade.student_id == student_id:
                    grades_list.append(grade.grade)
                    gpa = calculate_gpa(grades_list)
            return {
            'student_name': student.name,
            'student_mat_no': student.mat_no,
            'CGPA': gpa
            }, 200
        elif username == student.mat_no :
            grades_list = []
            GradeList = Grade.query.all()
            for grade in GradeList:
                if grade.student_id == student_id:
                    grades_list.append(grade.grade)
                    gpa = calculate_gpa(grades_list)
            return {
            'student_name': student.name,
            'student_mat_no': student.mat_no,
            'CGPA': gpa
            }, 200
        else:
            return {"error" : "You are not Authorised to perform this action or Student has no GPA"} , HTTPStatus.NOT_FOUND
            

@grade_namespace.route('/<int:course_id>/<int:student_id>')
class GradeByCourseAndStudent(Resource):
    @grade_namespace.doc(
        description= " Edit a Particular Student Grade in a Specific Course"
    )
    @jwt_required()
    @grade_namespace.expect(grade_model)
    @grade_namespace.marshal_with(grade_model)
    def put(self, course_id, student_id):
        """
        Edit a student's grade in a specific course
        """
        to_update = Grade.query.filter_by(course_id=course_id, student_id=student_id).first()
        if to_update is None:
            return {"message": "Grade not found"}, HTTPStatus.NOT_FOUND
        
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return 'You are not Authorised to perform this action' , HTTPStatus.FORBIDDEN
        else:
            data = grade_namespace.payload
            to_update.grade = data["grade"]
            to_update.edit()
            return to_update, HTTPStatus.OK

@grade_namespace.route("/grade")
class GetGrades(Resource):
    
    @grade_namespace.marshal_with(grade_model)
    @jwt_required()
    @grade_namespace.doc(
        description= " Get all Grades as a Teacher"
    )
    def get(self):
        """
            Get all Grades as teacher
        """
        username = get_jwt_identity()
        user = Teacher.query.filter_by(username=username).first()
        if (user is None):
           return {"Error": "You are not Authorised to perform this action"}, HTTPStatus.FORBIDDEN
        else:
            grade = Grade.query.all()
            return grade, HTTPStatus.OK
    
    