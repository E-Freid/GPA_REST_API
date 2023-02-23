from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jti, get_jwt_identity, create_access_token
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256

from datetime import datetime
from datetime import timezone

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Models import UserModel, BlockListModel

blp = Blueprint("users", __name__, description="Operations on users.")


@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        email = user_data["email"]
        password = pbkdf2_sha256.hash(user_data["password"])
        user = UserModel(email=email, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return {"message": "User was created successfully.", "email": user.email}, 201
        except IntegrityError:
            abort(400, message="Email is already taken. Registration failed.")
        except SQLAlchemyError:
            abort(500, message="An error occurred while trying to register. Registration failed")


@blp.route("/login")
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter(UserModel.email == user_data["email"]).first()
        if user and pbkdf2_sha256.verify(user_data["password"], user.password):
            access_token = create_access_token(identity=user.id)
            return {"message": "Login successful.", "access_token" : access_token}, 200

        abort(401, message="Invalid email or password.")


@blp.route("/logout")
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        revoked_token = BlockListModel(jti=jti)
        try:
            db.session.add(revoked_token)
            db.session.commit()
            return {"message": "Logged out successfully."}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred.")


# for dev only, remove later
@blp.route("/dev/user")
class DevUser(MethodView):
    @blp.response(200, UserSchema(many=True))
    def get(self):
        return UserModel.query.all()

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        user = UserModel.query.get_or_404(user_id)
        jti = get_jwt()["jti"]
        revoked_token = BlockListModel(jti=jti)
        try:
            db.session.delete(user)
            db.session.add(revoked_token)
            db.session.commit()
            return {"message": "User was deleted."}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred while deleting.")