from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
import datetime
from .models import User
from . import db
from icecream import ic
from functools import wraps

auth = Blueprint('auth', __name__)

current_datetime = datetime.datetime.now().strftime('%d-%m-%Y %H:%M:%S')


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)
        elif current_user.user_group != 'admins' and current_user.user_group != 'Admins':
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


@auth.route('/login')
def login():
    return render_template('login.html')


@auth.route('/login', methods=['POST'])
def login_post():
    name = request.form.get('name')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(name=name).first()

    if not user or not check_password_hash(user.password, password):
        flash('Проверьте введенные данные или зарегистрируйтесь')
        return redirect(url_for('auth.login'))

    login_user(user, remember=remember)
    if ic(login_user(user)):
        user.last_login_date = datetime.datetime.now()
        db.session.commit()
    return redirect(url_for('main.index'))


@auth.route('/signup')
def signup():
    return render_template('signup.html')


@auth.route('/signup', methods=['POST'])
def signup_post():
    name = request.form.get('name')
    password = request.form.get('password')
    user_name = User.query.filter_by(name=name).first()
    invite = request.form.get('invite')
    if user_name:
        flash('Данный логин уже используется!')
        return redirect(url_for('auth.signup'))
    elif invite != 'd1a740a9-2012-4749-8d8d-43386e174714':
        flash('Неверный инвайт!')
        return redirect(url_for('auth.signup'))
    try:
        new_user = ic(User(name=name, password=generate_password_hash(password, method='scrypt'), user_group='RHTeam', active=True))
        db.session.add(new_user)
        db.session.commit()
        ic(new_user)
        ic(new_user.id)
    except Exception as e:
        ic(e)

    return redirect(url_for('auth.login'))


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))
