from sqlalchemy import Column, Integer#, String, Boolean
from sqlalchemy.orm import relationship
from model.base import db

class CourseUserLink(db.Model):
    __tablename__ = 'course_user_link'

    class_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, primary_key=True)

    classes = relationship('Class', back_populates='classes')
    users = relationship('User', back_populates='users')

    def json(self):
        return {'class_id': self.class_id,
                'user_id': self.user_id}

    def __repr__(self):
        attrs = ", ".join(f"{key}={value!r}" for key, value in vars(self).items())
        return f"{self.__class__.__name__}({attrs})"