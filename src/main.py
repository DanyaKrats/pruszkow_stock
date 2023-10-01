from fastapi import FastAPI
from sqladmin import Admin
from src.api.routes.router import base_router

from src.middleware.sqlalch_sess import AssyncSessionMiddleware
import ui.admin as ui
from src.buisness_logic.auth.auth import AdminAuthController
from src.di.providers import provide_async_session, provide_db
# from src.di.db import 


def get_application(test: bool = False):
    application = FastAPI()
    db_engine = provide_db()
    # application.add_middleware(middleware_class=AssyncSessionMiddleware)
    application.include_router(base_router)
    setup_di(application, db_engine)
    return application
    
def setup_di(application, db_engine):    
    admin = Admin(
        application,
        db_engine,
        # authentication_backend=AdminAuthController(
        #     secret_key='123123',
        #     session=provide_async_session(db_engine)
        # )
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




