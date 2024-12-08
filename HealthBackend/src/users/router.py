from fastapi import APIRouter, Response, status
from src.database.session import SessionDep
from sqlalchemy import select
from src.users.models import User
from src.users.schemas import UserSchema

router = APIRouter(prefix="/users")


@router.get("/")
async def get_all_users(session: SessionDep):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.post(path="/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
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
    return new_user


@router.get("/{user_id}")
async def get_all_users(user_id: int, session: SessionDep):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user
