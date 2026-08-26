import logging
from werkzeug.exceptions import HTTPException
from app.utils.responses import error

logger = logging.getLogger("skillgap")


def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(e):
        return error("Bad request", 400)

    @app.errorhandler(401)
    def unauthorized(e):
        return error("Unauthorized. Please log in.", 401)

    @app.errorhandler(403)
    def forbidden(e):
        return error("You do not have permission to perform this action.", 403)

    @app.errorhandler(404)
    def not_found(e):
        return error("Resource not found", 404)

    @app.errorhandler(409)
    def conflict(e):
        return error("Conflict with existing resource", 409)

    @app.errorhandler(413)
    def too_large(e):
        return error("Uploaded file is too large", 413)

    @app.errorhandler(422)
    def unprocessable(e):
        return error("Validation error", 422)

    @app.errorhandler(HTTPException)
    def handle_http_exception(e):
        return error(e.description or "Request error", e.code or 400)

    @app.errorhandler(Exception)
    def handle_unexpected_error(e):
        logger.exception("Unexpected server error: %s", e)
        # Never leak stack traces to the client in production
        return error("An unexpected error occurred. Please try again later.", 500)
