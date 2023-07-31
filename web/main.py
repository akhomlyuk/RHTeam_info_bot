import os
import logging
from flask import Blueprint, render_template, request, send_from_directory, redirect, url_for, flash
from flask_login import login_required, current_user
from icecream import ic
from .db_functions import show_users, set_admins_group, set_users_group, delete_user
from .auth import admin_required
from .models import User
from .helpers import images_to_index

main = Blueprint('main', __name__)

brief_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'brief'))
blacklist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'blacklist'))
next_event_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'next'))
todo_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'notes', 'todo'))
log_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs', 'web.log'))

logging.basicConfig(level=logging.INFO, filename=log_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/')
def index():
    img_list = images_to_index()
    ic(img_list)
    return render_template('index.html', images=img_list)


@main.route('/adm')
@login_required
def admin_panel():
    show_user = show_users()
    return render_template('admin.html', users=show_user, user_group=User.user_group)


@main.route('/editor')
@login_required
def editor_panel():
    try:
        with open(next_event_path, 'r', encoding='UTF-8', newline='') as file:
            content = file.read()
        with open(todo_path, 'r', encoding='UTF-8', newline='') as todo:
            todo = todo.read()
        with open(blacklist_path, 'r', encoding='UTF-8', newline='') as blacklist:
            blacklist = blacklist.read()
        return render_template('editor.html', user_group=User.user_group,  blacklist=blacklist, next_event=content, todo_list=todo)
    except Exception as e:
        ic(e)


@main.route('/set_admins_group/<int:user_id>')
@admin_required
def set_admins_group_route(user_id):
    set_admins_group(user_id)
    flash('Группа успешно изменена')
    return redirect(url_for('main.admin_panel'))


@main.route('/set_users_group/<int:user_id>')
@admin_required
def set_users_group_route(user_id):
    set_users_group(user_id)
    flash('Группа успешно изменена')
    return redirect(url_for('main.admin_panel'))


@main.route('/delete_user/<int:user_id>')
@admin_required
def delete_user_route(user_id):
    delete_user(user_id)
    flash('Пользователь удален')
    return redirect(url_for('main.admin_panel'))


@main.route('/nextevent', methods=['POST'])
@admin_required
def save_nextevent():
    updated_content = request.form['next_event']
    with open(next_event_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', next_event=updated_content, name=current_user.name)


@main.route('/saveblacklist', methods=['POST'])
@admin_required
def save_blacklist():
    updated_content = request.form['blacklist']
    with open(blacklist_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', blacklist=updated_content, name=current_user.name)


@main.route('/savebrief', methods=['POST'])
@admin_required
def save_brief():
    updated_content = request.form['brief']
    with open(brief_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', brief=updated_content, name=current_user.name)


@main.route('/todolist', methods=['POST'])
@admin_required
def save_todolist():
    updated_content = request.form['todo_list']
    with open(todo_path, 'w', encoding='UTF-8', newline='') as file:
        file.write(updated_content)
    return render_template('success.html', todo_list=updated_content, name=current_user.name)


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
