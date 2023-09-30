from src.database.tables.cargo import Cargo, DangerousType
from sqladmin import ModelView


class CargoView(ModelView, model = Cargo):
    # icon =
    column_list =[
        Cargo.id,
        Cargo.client,
        Cargo.name
    ]

class DangerousTypeView(ModelView,  model = DangerousType):
    # icon =
    column_list =[
        DangerousType.id,
        DangerousType.name,
    ]