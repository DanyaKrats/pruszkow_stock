from fastapi import FastAPI
from sqladmin import Admin
from ui.admin import setup_views
from src.router import base_router



def get_application(test: bool = False):
    application = FastAPI()
    application.include_router(base_router)
    setup_di(application)
    return application
    
def setup_di(application):    
    admin = Admin(
        application,
    )
    setup_views(admin)
    


app = get_application()




