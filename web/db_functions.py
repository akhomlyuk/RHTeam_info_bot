from .models import User


def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        # users_list.append([user.id, user.name, user.group, user.active])
        # users_list.append(f"ID: <b>{user.id}</b> Имя: <b>{user.name}</b> Группа: <b>{user.group}</b> Активен: <b>{user.active}</b>")
        # users_list.append(f"ID: {user.id} Имя: {user.name} Группа: {user.group} Активен: {user.active}")
        users_list.append({'id': user.id, 'name': user.name, 'group': user.group, 'active': user.active})
    return users_list
