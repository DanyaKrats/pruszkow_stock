from src.database.tables.users import User, Role
from sqladmin import ModelView


class UserView(ModelView, model = User):
    # icon =
    column_list =[
        User.name,
        User.roles,
        User.client,
    ]

class RoleView(ModelView, model = Role):
    # icon =
    column_list =[
        Role.name,
        Role.users,
    ]