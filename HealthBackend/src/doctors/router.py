from fastapi import APIRouter, status
from sqlalchemy import select, update

from src.database.session import SessionDep
from src.doctors.models import Doctor
from src.doctors.schemas import DoctorSchema

# from src.users.schemas import UserSchema, UserPatchSchema

router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/")
async def get_all_doctors(session: SessionDep) -> list[int]:
    query = select(Doctor)
    result = await session.execute(query)
    doctors = [d.id for d in result.scalars()]
    return doctors


@router.post("/")
async def add_doctor(session: SessionDep, data: DoctorSchema) -> DoctorSchema:
    data = data.model_dump()
    new_doctor = Doctor(
        id=data['id']
    )
    session.add(new_doctor)
    await session.commit()
    return new_doctor

