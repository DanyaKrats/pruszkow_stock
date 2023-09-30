from fastapi import FastAPI
from sqladmin import Admin
from src.router import base_router
from sqlalchemy import create_engine
import ui.admin as ui
def create_database_engine(db_url = "postgresql://postgres:postgres@localhost/pruszkow_stock"):
    engine = create_engine(db_url)
    return engine

def get_application(test: bool = False):
    application = FastAPI()
    db_engine = create_database_engine()
    application.include_router(base_router)
    setup_di(application, db_engine)
    return application
    
def setup_di(application, db_engine):    
    admin = Admin(
        application,
        db_engine,
    )

    admin.add_model_view(ui.CargoView)
    admin.add_model_view(ui.DangerousTypeView)
    # admin.add_base_view(ui.SeparationLine)

    admin.add_model_view(ui.ClientView)
    admin.add_model_view(ui.SenderView)
    admin.add_model_view(ui.RecipientView)
    # admin.add_base_view(ui.SeparationLine)

    admin.add_model_view(ui.UserView)
    admin.add_model_view(ui.RoleView)
    


app = get_application()




