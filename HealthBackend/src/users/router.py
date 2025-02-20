from fastapi import APIRouter, status
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database.session import SessionDep
from src.users.models import User
from src.users.schemas import UserSchema, UserPatchSchema

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all_users(session: SessionDep,
                        with_diseases: bool = None,
                        free: bool = None):
    query = select(User)
    if with_diseases:
        query = query.options(selectinload(User.diseases))
    if free:
        query = query.where(User.doctor_id == None)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.post(path="/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def add_user(data: UserSchema, session: SessionDep):
    data = data.model_dump()
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
async def get_user(user_id: int, session: SessionDep):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


@router.patch("/{user_id}")
async def update_user(user_id: int,
                      session: SessionDep,
                      body: UserPatchSchema):
    try:
        update_data = body.model_dump(exclude_none=True)
        if update_data.get('doctor_id', None) == 0:
            update_data['doctor_id'] = None
        query = update(User).where(User.id == user_id).values(**update_data)
        await session.execute(query)
    except Exception as ex:
        await session.rollback()
        return {"success": False, "message": ex}
    else:
        await session.commit()
        return {"success": True}


@router.get("/by_doctor/{doctor_id}")
async def get_doctors_users(doctor_id: int,
                            session: SessionDep,
                            with_diseases: bool = False
                            ):
    query = select(User).where(User.doctor_id == doctor_id)
    if with_diseases:
        query = query.options(
            selectinload(User.diseases))
    result = await session.execute(query)
    users = result.scalars().all()
    return users
