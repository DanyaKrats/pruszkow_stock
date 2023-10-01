from fastapi import APIRouter, Request
from src.di.providers import provide_async_session
from src.database.repos.user import UserRepository, RoleRepository

user_router = APIRouter(
    tags=["users"], prefix='/user'
)


@user_router.get("/", response_model=dict)
async def get_all_users(request:Request):
    session = provide_async_session()
    user_repo = UserRepository(session)
    responce = await user_repo.get_all_users()
    responce = [{'name':user.name, 'email':user.email}for user in responce]
    session.close()
    return {"message": responce}


