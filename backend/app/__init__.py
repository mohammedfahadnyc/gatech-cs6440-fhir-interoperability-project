from flask import Flask, jsonify
from flask_jwt_extended import JWTManager

from app.config import Config
from app.db.database import db
from app.services.seed_service import ensure_seed_data

jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Central app wiring lives here so the backend can boot from `python run.py`.
    db.init_app(app)
    jwt.init_app(app)

    from app.routes.auth_routes import auth_bp
    from app.routes.chart_routes import chart_bp
    from app.routes.import_routes import import_bp
    from app.routes.patient_routes import patient_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(patient_bp, url_prefix="/patients")
    app.register_blueprint(chart_bp, url_prefix="/patients")
    app.register_blueprint(import_bp, url_prefix="/emr")

    @app.route("/health", methods=["GET"])
    def health_check():
        return jsonify({"status": "ok"})

    with app.app_context():
        # Keep the project immediately runnable without a separate migration step.
        db.create_all()
        if app.config.get("AUTO_SEED"):
            ensure_seed_data()

    return app
