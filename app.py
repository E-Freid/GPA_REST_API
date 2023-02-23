import os
from dotenv import load_dotenv

from flask import Flask
from flask_smorest import Api
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

from db import db
from Models import BlockListModel


from Resources.user import blp as UserBlueprint
from Resources.course import blp as CourseBlueprint
from Resources.gpa import blp as GpaBlueprint

def create_app(db_url=None):
    # declare app
    app = Flask(__name__)
    load_dotenv()

    # configure the app
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "grades REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "eli")

    # initialization
    db.init_app(app)
    migrate = Migrate(app, db, compare_type=True)
    api = Api(app)
    jwt = JWTManager(app)

    # jwt token error handling
    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        if BlockListModel.query.filter(BlockListModel.jti == jwt_payload["jti"]).first():
            return True
        return False


    # register Blueprints
    api.register_blueprint(UserBlueprint)
    api.register_blueprint(CourseBlueprint)
    api.register_blueprint(GpaBlueprint)

    return app