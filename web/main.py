import os
import logging
from flask import Blueprint, render_template, request, send_from_directory
from flask_login import login_required, current_user
from .db_functions import show_users

main = Blueprint('main', __name__)

brief_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'brief'))
next_event_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'next'))
todo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'todo'))
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'web.log'))
logging.basicConfig(level=logging.INFO, filename=log_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/')
def index():
    with open(next_event_path, 'r', encoding='UTF-8', newline='') as file:
        content = file.read()
    with open(todo_path, 'r', encoding='UTF-8', newline='') as todo:
        todo = todo.read()
    return render_template('index.html', next_event=content, todo_list=todo)


@main.route('/adm')
@login_required
def admin_panel():
    show_user = show_users()
    return render_template('admin.html', users=show_user)


@main.route('/nextevent', methods=['POST'])
@login_required
def save_nextevent():
    updated_content = request.form['next_event']
    with open(next_event_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', next_event=updated_content)


@main.route('/savebrief', methods=['POST'])
@login_required
def save_brief():
    updated_content = request.form['brief']
    with open(brief_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', brief=updated_content)


@main.route('/todolist', methods=['POST'])
@login_required
def save_todolist():
    updated_content = request.form['todo_list']
    with open(todo_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', todo_list=updated_content)


@main.route('/settings')
@login_required
def show_settings():
    with open(brief_path, 'r', encoding='UTF-8', newline='') as file:
        brief = file.read()
    return render_template('settings.html', brief=brief)


@main.route('/profile')
@login_required
def profile():
    invite = 'd1a740a9-2012-4749-8d8d-43386e174714'
    return render_template('profile.html', invite=invite, name=current_user.name)
