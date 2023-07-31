from icecream import ic
from .models import User
from . import db


def show_users():
    try:
        users = User.query.all()
        users_list = []
        for user in users:
            if user is not None:
                users_list.append({'id': user.id, 'name': user.name, 'user_group': user.user_group, 'active': user.active,
                                   'isadmin': user.isadmin, 'last_login_date': user.last_login_date})
        return users_list
    except Exception as e:
        ic(e)


def set_admins_group(user_id: int):
    user = User.query.get(user_id)
    user.user_group = 'Admins'
    db.session.commit()


def set_users_group(user_id: int):
    user = User.query.get(user_id)
    user.user_group = 'RHTeam'
    db.session.commit()


def delete_user(user_id: int):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
