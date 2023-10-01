import bcrypt
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from typing import Union
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, SecretStr
from src.database.tables.users import User
from .jwt_service import JWTService
from src.database.repos.user import UserRepository


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)

def make_token(user) -> str:
    return ''


class AdminCredentialsDTO(BaseModel):
    username: str
    password: SecretStr


class AdminAuthController(AuthenticationBackend):
    def __init__(self, secret_key: str, session) -> None:
        self.session = session
        super().__init__(secret_key=secret_key,)

    async def login(self, request: Request) -> bool:
        data_from_form = await request.form()
        try:
            username=data_from_form.get("username")
            password=data_from_form.get("password")
            user_repo = UserRepository(session=self.session)
            user:User = user_repo.get_user_by_username(username)
            if check_password(password, user.password_hashed):
                token = self.jwt.encode_jwt(payload={'user_id': user.id, 'aud':[role.name for role in user.roles]})
                request.session.update({"Token": token})
                if "Admin" in [role.name for role in user.roles]:
                    return True
                else:
                    return RedirectResponse(f"/")
            else:
                return False
            
        except Exception as e:
            return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> Union[None, RedirectResponse]:
        token = request.session.get("Token")

        if self.jwt.decode_token(token=token, aud="Admin"):
            return None
        else:
            # return None
            return RedirectResponse(f"admin/login")
        



class AdminAuthService:
    def __init__(self) -> None:
        pass
    
    async def authorize(
        self, credentials: AdminCredentialsDTO, exp_time: int = 900
    ) -> Union[str, None]:
        pass    

    async def authenticate(self, token: str) -> Union[None, RedirectResponse]:
        if await self.jwt_service.verify_token(token=token, aud="oidc:admin_ui"):
            return None
        else:
            # return None
            return RedirectResponse(f"/admin/login")
        
