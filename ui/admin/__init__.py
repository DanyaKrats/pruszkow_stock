from .cargo import CargoView, DangerousTypeView
from sqladmin import Admin

all_views = [
    CargoView, 
    DangerousTypeView,
]

def setup_views(admin:Admin):
    for view in all_views:
        admin.add_view(view)