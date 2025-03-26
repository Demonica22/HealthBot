from fastapi import APIRouter, status

from src.database.session import SessionDep
from src.users.schemas import UserSchema, UserPatchSchema
from src.users.service import UserService

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/")
async def get_all_users(session: SessionDep,
                        with_diseases: bool = None,
                        free: bool = None):
    return await UserService.get_all_users(session, with_diseases, free)


@router.post(path="/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def add_user(data: UserSchema, session: SessionDep):
    return await UserService.create_user(data, session)


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep):
    return await UserService.get_user(user_id, session)


@router.patch("/{user_id}")
async def update_user(user_id: int,
                      session: SessionDep,
                      body: UserPatchSchema):
    return await UserService.update_user(user_id, body=body, db_session=session)


@router.get("/by_doctor/{doctor_id}")
async def get_doctors_users(doctor_id: int,
                            session: SessionDep,
                            with_diseases: bool = False
                            ):
    return await UserService.get_users_by_doctor(doctor_id=doctor_id, db_session=session, with_diseases=with_diseases)
