from typing import Any, Dict, Optional, Tuple, Union

from sqlalchemy import exc, exists, insert, select, update, delete
from sqlalchemy.engine.result import ChunkedIteratorResult
from sqlalchemy.ext.asyncio import AsyncSession
from src.database.tables.users import User, users_roles, Role
import bcrypt

def hash_password(password:str):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password

def check_password(input_password, stored_password):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_password)

class UserRepository():
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def get_all_users(self):
        query = await self.session.execute(select(User))
        query = query.all()
        return [user[0] for user in query]


    async def get_username_by_id(self, id: int) -> str:
        users = await self.session.execute(select(User).where(User.id == id))
        result = users.first()
        result = result[0].username
        return result

    async def get_user_by_username(self, username: str) -> User:
        try:
            user = await self.session.execute(
                select(User)
                .where(User.username == username)
            )
            user = user.first()

            return user[0]
        except:
            raise ValueError

    def __repr__(self) -> str:
        return "User repository"

    async def create(
        self, 
        name,
        email,
        password
    ) -> None:
        
        password_hashed = hash_password(password)
        user = await self.session.execute(insert(User).values({'name':name, 'email':email, 'password_hashed':password_hashed}).returning(User))
        return user.first()[0]

    async def add_role(
        self,
        user_id,
        role_id,
    ) -> None:
        
        await self.session.execute(insert(users_roles).values(user_id =user_id, role_id =role_id))


class RoleRepository():
    def __init__(self, session:AsyncSession) -> None:
        self.session = session

    async def get_all_roles(self):
        query = await self.session.execute(select(Role))
        query = query.all()
        return [user[0] for user in query]


    async def get_role_by_id(self, id: int) -> str:
        role = await self.session.execute(select(Role).where(Role.id == id))
        result = role.first()[0]
        return result

    async def get_role_by_name(self, name: str) -> str:
        role = await self.session.execute(select(Role).where(Role.name == name))
        result = role.first()[0]
        return result

    async def create(
        self, 
        name,
    ) -> None:
        role = await self.session.execute(insert(Role).values({'name':name}).returning(Role))
        return role.first()[0]