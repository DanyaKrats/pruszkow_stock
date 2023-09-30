from .cargo import CargoView, DangerousTypeView
from .client import ClientView, SenderView, RecipientView
from sqladmin import Admin

all_views = [
    CargoView, 
    DangerousTypeView,
    ClientView,
    SenderView,
    RecipientView
]

def setup_views(admin:Admin):
    for view in all_views:
        admin.add_view(view)