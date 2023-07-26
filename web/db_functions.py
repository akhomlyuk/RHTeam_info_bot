from .models import User
from . import db


def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({'id': user.id, 'name': user.name, 'group': user.group, 'active': user.active})
    return users_list


def set_admins_group(user_id: int):
    user = User.query.get(user_id)
    user.group = 'Admins'
    db.session.commit()


def set_users_group(user_id: int):
    user = User.query.get(user_id)
    user.group = 'Users'
    db.session.commit()


def delete_user(user_id: int):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
