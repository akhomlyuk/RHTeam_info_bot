from .models import User


def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        # users_list.append([user.id, user.name, user.group, user.active])
        users_list.append(f"ID: <b>{user.id}</b> Имя: <b>{user.name}</b> Группа: <b>{user.group}</b> Активен: <b>{user.active}</b>")

    return users_list
