SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "FHIR Diabetes Interoperability Bridge API",
        "description": "FHIR-first diabetes middleware with JWT auth, chart APIs, and FHIR bundle export.",
        "version": "1.0.0",
    },
    "basePath": "/",
    "schemes": ["http"],
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "JWT Authorization header using the Bearer scheme. Example: 'Bearer <token>'",
        }
    },
}


SWAGGER_CONFIG = {
    "headers": [],
    "specs": [
        {
            "endpoint": "apispec",
            "route": "/apispec.json",
            "rule_filter": lambda rule: True,
            "model_filter": lambda tag: True,
        }
    ],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/apidocs/",
}
