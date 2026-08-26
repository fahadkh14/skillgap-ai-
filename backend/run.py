from app import create_app

app = create_app()

if __name__ == "__main__":
    # Development-only entrypoint. Production uses Gunicorn (see Dockerfile).
    app.run(host="0.0.0.0", port=5678, debug=app.config["DEBUG"])
