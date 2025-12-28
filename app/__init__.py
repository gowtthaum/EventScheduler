from flask import Flask, redirect, url_for
from app.models import db
from app.routes.reports import reports_bp


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    with app.app_context():
        db.create_all()


    from app.routes.events import events_bp
    from app.routes.resources import resources_bp
    from app.routes.allocations import allocations_bp
    from app.routes.home import home_bp
    

    
    app.register_blueprint(home_bp) 
    app.register_blueprint(events_bp)
    app.register_blueprint(resources_bp)
    app.register_blueprint(allocations_bp)
    app.register_blueprint(reports_bp)
    

    

    return app
