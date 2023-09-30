from .cargo import CargoView, DangerousTypeView
from .client import ClientView, SenderView, RecipientView
from .users import UserView, RoleView
from sqladmin import BaseView, expose

all_views = {
    1:CargoView, 
    2:DangerousTypeView,
    3:ClientView,
    4:SenderView,
    5:RecipientView,
    6:UserView,
    7:RoleView,
}

class SeparationLine(BaseView):
    name = " "

    # icon = "fa-solid fa-chart-line"
    # @no_type_check
    @expose("/", methods=["GET"])
    def test_page(self, request) -> None:
        return None
