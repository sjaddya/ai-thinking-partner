from flask import Blueprint, Flask, send_from_directory

from config import Config
from habits.routes import habits_bp

journal_bp = Blueprint("journal", __name__)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.register_blueprint(habits_bp, url_prefix="/habits")
    app.register_blueprint(journal_bp, url_prefix="/journal")

    @app.get("/")
    def tracker_page():
        return send_from_directory("static", "index.html")

    @app.get("/habits_manage.html")
    @app.get("/manage")
    def manage_page():
        return send_from_directory("static", "habits_manage.html")

    @app.get("/health")
    def health():
        return {"status": "ok"}, 200

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=app.config["DEBUG"])
