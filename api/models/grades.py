from ..utils import db
from enum import Enum
from datetime import datetime

class Grade(db.Model):
    __tablename__ = 'grades'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    grade = db.Column(db.Float, nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    
    def __repr__(self):
        return f"<Course {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
    
    def edit(self):
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    