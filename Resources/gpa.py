from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt_identity

from Models import UserModel

from schemas import GpaSchema


blp = Blueprint("gpa", __name__, description="GPA operations. MUST CONTAIN JWT")


# helper function
def calculate_gpa(courses):
    up = 0
    down = 0
    for course in courses:
        up += course.grade * course.points
        down += course.points
    result = up/down
    return round(result, 3)


@blp.route("/user/gpa")
class UserGpa(MethodView):
    @jwt_required()
    @blp.response(200, GpaSchema)
    def get(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        try:
            return {"gpa": calculate_gpa(user.courses)}
        except ZeroDivisionError:
            abort(400, message="Invalid course calculation.")

