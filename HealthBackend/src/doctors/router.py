from fastapi import APIRouter

from src.database.session import SessionDep
from src.doctors.schemas import DoctorSchema
from src.doctors.service import DoctorService

router = APIRouter(prefix="/doctor", tags=["Doctor"])


@router.get("/")
async def get_all_doctors(session: SessionDep) -> list[int]:
    return await DoctorService.get_all_doctors(session)


@router.post("/")
async def add_doctor(session: SessionDep, data: DoctorSchema) -> DoctorSchema:
    return await DoctorService.add_doctor(session=session, data=data)
