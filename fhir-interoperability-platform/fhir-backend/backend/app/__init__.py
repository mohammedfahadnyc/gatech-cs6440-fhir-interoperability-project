from flask import Flask, jsonify
from flasgger import Swagger
from flask_jwt_extended import JWTManager

from app.config import Config
from app.db.database import db
from app.docs import SWAGGER_CONFIG, SWAGGER_TEMPLATE
from app.services.patient_compat_service import (
    ensure_patient_demo_columns,
    migrate_existing_patients_to_internal,
)
from app.services.seed_service import ensure_seed_data

jwt = JWTManager()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Central app wiring lives here so the backend can boot from `python run.py`.
    db.init_app(app)
    jwt.init_app(app)
    Swagger(app, config=SWAGGER_CONFIG, template=SWAGGER_TEMPLATE)

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
        """
        Health check endpoint.
        ---
        tags:
          - System
        responses:
          200:
            description: API is healthy
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: ok
        """
        return jsonify({"status": "ok"})

    with app.app_context():
        # Keep the project immediately runnable without a separate migration step.
        db.create_all()
        ensure_patient_demo_columns()
        migrate_existing_patients_to_internal()
        if app.config.get("AUTO_SEED"):
            ensure_seed_data()

    return app
