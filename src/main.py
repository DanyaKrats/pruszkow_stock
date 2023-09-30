from fastapi import FastAPI
from sqladmin import Admin
from ui.admin import setup_views
from src.router import base_router
from sqlalchemy import create_engine

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
    setup_views(admin)
    


app = get_application()




