from .models import User


def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        users_list.append({'id': user.id, 'name': user.name, 'group': user.group, 'active': user.active})
    return users_list
