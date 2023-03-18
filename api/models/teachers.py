from ..utils import db

class Teacher(db.Model):
    __tablename__='teachers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(45), nullable=False, unique=True)
    username = db.Column(db.String(45), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password_hash = db.Column(db.Text(), nullable=False)
    courses = db.relationship('Course', backref='teacher', lazy=True)
    user_type = db.Column(db.String(20))
    Grades = db.relationship('Grade', backref='teacher', lazy=True)
    
    __mapper_args__ = {
        'polymorphic_on': user_type,
        'polymorphic_identity': 'teacher'
    }
    
    def __repr__(self):
        return f"<Teacher {self.username}>"
    
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