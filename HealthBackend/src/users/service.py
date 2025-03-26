import logging

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload

from src.database.session import SessionDep
from src.users.models import User
from src.users.schemas import UserSchema, UserPatchSchema


class UserService:
    @staticmethod
    async def create_user(data: UserSchema, db_session: SessionDep):
        data = data.model_dump()
        new_user = User(
            id=data['id'],
            name=data['name'],
            gender=data['gender'],
            language=data['language'],
            weight=data['weight'],
            height=data['height'],
        )
        db_session.add(new_user)
        await db_session.commit()
        return new_user

    @staticmethod
    async def get_user(user_id: int, db_session: SessionDep):
        query = select(User).where(User.id == user_id)
        result = await db_session.execute(query)
        user = result.scalars().first()
        return user

    @staticmethod
    async def get_all_users(db_session: SessionDep,
                            with_diseases=None,
                            free=None):
        query = select(User)
        if with_diseases:
            query = query.options(selectinload(User.diseases))
        if free:
            query = query.where(User.doctor_id == None)
        result = await db_session.execute(query)
        users = result.scalars().all()
        return users

    @staticmethod
    async def update_user(user_id: int, body: UserPatchSchema, db_session: SessionDep):
        try:
            update_data = body.model_dump(exclude_none=True)
            if update_data.get('doctor_id', None) == 0:
                update_data['doctor_id'] = None
            query = update(User).where(User.id == user_id).values(**update_data)
            await db_session.execute(query)
        except Exception as ex:
            logging.error(ex)
            await db_session.rollback()
            return {"success": False, "message": ex}
        else:
            await db_session.commit()
            return {"success": True}

    @staticmethod
    async def get_users_by_doctor(doctor_id: int, with_diseases: bool, db_session: SessionDep):
        query = select(User).where(User.doctor_id == doctor_id)
        if with_diseases:
            query = query.options(
                selectinload(User.diseases))
        result = await db_session.execute(query)
        users = result.scalars().all()
        return users
