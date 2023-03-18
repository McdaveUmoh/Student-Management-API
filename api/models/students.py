from ..utils import db

class Student(db.Model):
    __tablename__='students'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    mat_no = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'))
    
    def __repr__(self):
        return f"<Student {self.mat_no}>"
    
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