from ..utils import db
from enum import Enum
from datetime import datetime
import json
from sqlalchemy.ext.mutable import Mutable
from sqlalchemy.types import TypeDecorator, VARCHAR


class JSONEncodedDict(TypeDecorator):
    """Represents an immutable structure as a json-encoded string."""

    impl = VARCHAR

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value


class MutableList(Mutable, list):
    """A mutable list."""

    @classmethod
    def coerce(cls, key, value):
        """Convert plain lists to MutableList."""
        if not isinstance(value, MutableList):
            if isinstance(value, list):
                return MutableList(value)
            return Mutable.coerce(key, value)
        else:
            return value

    def append(self, value):
        """Detect append event and emit change event."""
        list.append(self, value)
        self.changed()

    def remove(self, value):
        """Detect remove event and emit change event."""
        list.remove(self, value)
        self.changed()

    def extend(self, iterable):
        """Detect extend event and emit change event."""
        list.extend(self, iterable)
        self.changed()

    def insert(self, index, value):
        """Detect insert event and emit change event."""
        list.insert(self, index, value)
        self.changed()

class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    course_unit = db.Column(db.Integer)
    teacher_name = db.Column(db.String(50), nullable=False)
    students = db.Column(MutableList.as_mutable(JSONEncodedDict))
    student= db.relationship('Student', backref='course', lazy=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    def __repr__(self):
        return f"<Course {self.id}>"
    
    def save(self):
        db.session.add(self)
        db.session.commit()
        
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)
    