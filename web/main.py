import os
import logging
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from brief import *

main = Blueprint('main', __name__)

next_event_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'next'))
todo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'todo'))
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'web.log'))
logging.basicConfig(level=logging.INFO, filename=log_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@main.route('/')
def index():
    with open(next_event_path, 'r', encoding='UTF-8', newline='') as file:
        content = file.read()
    with open(todo_path, 'r', encoding='UTF-8', newline='') as todo:
        todo = todo.read()
    return render_template('index.html', next_event=content, todo_list=todo)


@main.route('/nextevent', methods=['POST'])
def save_nextevent():
    updated_content = request.form['next_event']
    with open(next_event_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', next_event=updated_content)


@main.route('/todolist', methods=['POST'])
def save_todolist():
    updated_content = request.form['todo_list']
    with open(todo_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', todo_list=updated_content)


@main.route('/settings')
def show_settings():
    # with open('config.py', 'r', encoding='UTF-8', newline='') as file:
    #     content = file.read()
    return render_template('settings.html', content=brief)


@main.route('/profile')
@login_required
def profile():
    invite = 'd1a740a9-2012-4749-8d8d-43386e174714'
    return render_template('profile.html', invite=invite, name=current_user.name)
