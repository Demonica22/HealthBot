from sqlalchemy import select

from src.database.session import SessionDep
from src.doctors.models import Doctor
from src.doctors.schemas import DoctorSchema


class DoctorService:

    @staticmethod
    async def get_all_doctors(session: SessionDep):
        query = select(Doctor)
        result = await session.execute(query)
        doctors = [d.id for d in result.scalars()]
        return doctors

    @staticmethod
    async def add_doctor(session: SessionDep, data: DoctorSchema):
        data = data.model_dump()
        new_doctor = Doctor(
            id=data['id']
        )
        session.add(new_doctor)
        await session.commit()
        return new_doctor
