from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()


def page_not_found(e):
    return render_template('login.html'), 302


def create_app():
    app = Flask(__name__)
    app.register_error_handler(404, page_not_found)
    app.config['SECRET_KEY'] = '33bf3cd3-ad1c-4429-b636-a807fc084e92_20ef441b-a7f2-4207-b0dc-543ca0d37aa2'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .models import User
    with app.app_context():
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    return app
