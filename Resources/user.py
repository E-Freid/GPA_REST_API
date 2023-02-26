import os
from dotenv import load_dotenv
from datetime import datetime

from flask import request
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask_jwt_extended import jwt_required, get_jwt, get_jwt_identity, create_access_token
from schemas import UserSchema
from passlib.hash import pbkdf2_sha256

from db import db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from Models import UserModel, BlockListModel

blp = Blueprint("users", __name__, description="Operations on users.")

load_dotenv()
clean_secret_key = os.getenv("CLEANUP_SECRET_KEY")

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
        exp = get_jwt()["exp"]
        revoked_token = BlockListModel(jti=jti, exp=datetime.utcfromtimestamp(exp))
        try:
            db.session.add(revoked_token)
            db.session.commit()
            return {"message": "Logged out successfully."}, 200
        except SQLAlchemyError:
            abort(500, message="An error occurred.")


@blp.route("/cleanup")
class CleanRevokedTokens(MethodView):
    @blp.response(200, description="Cleans the expired tokens from the blocklist. must contain special key in header")
    def post(self):
        now = datetime.utcnow()
        try:
            key = request.headers["clean_secret_key"]
            expired_tokens = BlockListModel.query.filter(BlockListModel.exp <= now).all()
            for token in expired_tokens:
                db.session.delete(token)
            db.session.commit()
            return {"message": "clean up was successful"}, 200
        except KeyError:
            abort(401, message="Not authorized")

        except SQLAlchemyError:
            abort(500, message="Error occurred with database.")