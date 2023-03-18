from .teachers import Teacher
from ..utils import db

class Admin(Teacher):
    __tablename__ = 'admin'
    id = db.Column(db.Integer(), db.ForeignKey('teachers.id'), primary_key=True)

    __mapper_args__ = {
        'polymorphic_identity': 'admin'
    }
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)