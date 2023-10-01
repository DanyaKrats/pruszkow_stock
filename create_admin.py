from src.di.providers import provide_async_session
from src.database.repos.user import UserRepository, RoleRepository

async def create_admin():
    session = provide_async_session()
    user_repo = UserRepository(session)
    role_repo = RoleRepository(session)
    user = await user_repo.create(
        name = "Admin",
        email = "admin@example.com",
        password = "admin",
        )
    try:
        role = await role_repo.get_role_by_name("Admin")
    except:
        role = await role_repo.create(name="Admin")
    await user_repo.add_role(user_id=user.id, role_id=role.id)

    await session.commit()
    await session.close()

    print('''
        name = "Admin"\n
        email = "admin@example.com"\n
        password = "admin"\n
        ''')

if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    loop.run_until_complete(create_admin())