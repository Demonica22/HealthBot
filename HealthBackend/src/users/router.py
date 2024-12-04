from fastapi import APIRouter
from src.database.session import SessionDep
from sqlalchemy import select
from src.users.models import User

router = APIRouter(prefix="/users")


@router.get("/")
async def get_all_users(session: SessionDep):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.post("/")
async def add_user(data: dict, session: SessionDep):
    new_user = User(
        id=data['id'],
        name=data['name'],
        gender=data['gender'],
        language=data['language'],
        weight=data['weight'],
        height=data['height'],
    )
    session.add(new_user)
    await session.commit()


@router.get("/{user_id}")
async def get_all_users(user_id: int, session: SessionDep):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user
