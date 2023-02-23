from db import db


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(), nullable=False)

    courses = db.relationship("CourseModel", back_populates="user", cascade="all, delete")