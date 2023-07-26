from .models import User


def show_users():
    users = User.query.all()
    users_list = []
    for user in users:
        # users_list.append([user.id, user.name, user.group, user.active])
        users_list.append(f"ID: {user.id} Имя: {user.name} Группа: {user.group} Активен: {user.active}")

    return users_list
