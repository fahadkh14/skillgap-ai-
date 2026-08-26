import logging
import sys

from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import jwt, init_mongo


def configure_logging(app):
    log_level = logging.DEBUG if app.config["DEBUG"] else logging.INFO
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        stream=sys.stdout,
    )


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    configure_logging(app)
    logger = logging.getLogger("skillgap")

    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}}, supports_credentials=True)

    jwt.init_app(app)
    init_mongo(app)

    from app.routes.auth import auth_bp, is_token_revoked
    from app.routes.profile import profile_bp
    from app.routes.skills import skills_bp
    from app.routes.job_roles import job_roles_bp
    from app.routes.analysis import analysis_bp
    from app.routes.resume import resume_bp
    from app.routes.roadmap import roadmap_bp
    from app.routes.dashboard import dashboard_bp
    from app.routes.health import health_bp

    jwt.token_in_blocklist_loader(is_token_revoked)

    app.register_blueprint(auth_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(skills_bp)
    app.register_blueprint(job_roles_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(roadmap_bp)
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(health_bp)

    from app.middleware.error_handler import register_error_handlers
    register_error_handlers(app)

    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        from app.utils.responses import error
        return error("Session expired. Please log in again.", 401)

    @jwt.invalid_token_loader
    def invalid_token_callback(reason):
        from app.utils.responses import error
        return error("Invalid authentication token.", 401)

    @jwt.unauthorized_loader
    def missing_token_callback(reason):
        from app.utils.responses import error
        return error("Authentication is required to access this resource.", 401)

    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        from app.utils.responses import error
        return error("Session has been logged out. Please log in again.", 401)

    logger.info("SkillGap AI backend application started")

    return app
