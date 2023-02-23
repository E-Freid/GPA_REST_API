from flask_smorest import Blueprint, abort
from flask_jwt_extended import get_jwt_identity, jwt_required
from flask.views import MethodView
from sqlalchemy.exc import SQLAlchemyError

from schemas import CourseSchema, UpdateCourseSchema

from db import db
from Models import CourseModel, UserModel

blp = Blueprint("courses", __name__, description="Operations on courses. MUST CONTAIN JWT")


@blp.route("/user/course")
class CourseList(MethodView):
    @jwt_required()
    @blp.response(200, CourseSchema(many=True))
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        return user.courses

    @jwt_required()
    @blp.arguments(CourseSchema)
    def post(self, course_data):
        user_id = get_jwt_identity()
        course = CourseModel(user_id=user_id, **course_data)
        try:
            db.session.add(course)
            db.session.commit()
            return {"message": "Course added successfully."}, 201
        except SQLAlchemyError:
            abort(500, message="An error occurred.")


@blp.route("/user/course/<int:course_id>")
class Course(MethodView):
    @jwt_required()
    @blp.response(200, CourseSchema)
    def get(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        if course.user_id == get_jwt_identity():
            return course
        else:
            abort(401, message="You are not taking this course.")

    @jwt_required()
    @blp.arguments(UpdateCourseSchema)
    @blp.response(200, CourseSchema)
    def put(self, course_data, course_id):
        user_id = get_jwt_identity()
        course = CourseModel.query.get(course_id)
        if course:
            if course.user_id == user_id:
                course.name = course_data["name"]
                course.grade = course_data["grade"]
                course.points = course_data["points"]
            else:
                abort(401, message="You are not taking this course.")
        else:
            course = CourseModel(id=course_id, user_id=user_id, **course_data)

        try:
            db.session.add(course)
            db.session.commit()
            return course
        except SQLAlchemyError:
            abort(500, message="An error occurred.")

    @jwt_required()
    def delete(self, course_id):
        course = CourseModel.query.get_or_404(course_id)
        if course.user_id == get_jwt_identity():
            try:
                db.session.delete(course)
                db.session.commit()
                return {"message": "Course was deleted."}, 200
            except SQLAlchemyError:
                abort(500, message="An error occurred.")
        else:
            abort(401, message="You are not taking this course.")
