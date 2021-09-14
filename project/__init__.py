from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_swagger_ui import get_swaggerui_blueprint
from flask_migrate import Migrate, MigrateCommand

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'thisissecret'
    app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:12345678@localhost/doctor_appointment"
    
    db.init_app(app)
    migrate.init_app(app, db)

    from project.models import User

    #API Route
    from project.api.user import user_api_bp
    from project.api.doctor import doctor_api_bp
    from project.api.patient import patient_api_bp

    app.register_blueprint(user_api_bp, url_prefix="/user_api")
    app.register_blueprint(doctor_api_bp, url_prefix="/doctor_api")
    app.register_blueprint(patient_api_bp, url_prefix="/patient_api")

    ### swagger specific ###
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.json'
    SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={
            'app_name': "CMDs-Python-Flask-REST-API"
        }
    )
    app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)
    ### end swagger specific ###

    return app
