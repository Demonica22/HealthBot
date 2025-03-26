from fastapi import APIRouter, status, Request

from datetime import datetime

from src.database.session import SessionDep
from src.diseases.schemas import DiseaseSchemaAdd, DiseaseSchema
from src.diseases.enums import DiseasesResponseFormat, UserLanguage
from src.diseases.service import DiseasesService

router = APIRouter(prefix="/diseases", tags=['Diseases'])


@router.post("/",
             response_model=DiseaseSchema,
             status_code=status.HTTP_201_CREATED)
async def add_disease(data: DiseaseSchemaAdd, session: SessionDep):
    return await DiseasesService.add_disease(data, session)


@router.get("/{disease_id}")
async def get_disease(
        disease_id: int,
        session: SessionDep):
    return await DiseasesService.get_disease(disease_id, session)


@router.get("/for_user/{user_id}")
async def get_all_user_diseases(user_id: int,
                                session: SessionDep,
                                request: Request,
                                start_date: str = "-1",
                                response_format: DiseasesResponseFormat = DiseasesResponseFormat.json,
                                user_language: UserLanguage = UserLanguage.ru,
                                only_active: bool = False):
    return await DiseasesService.get_all_user_diseases(user_id=user_id,
                                                       session=session,
                                                       request=request,
                                                       start_date=start_date,
                                                       response_format=response_format,
                                                       user_language=user_language,
                                                       only_active=only_active)


@router.patch("/mark_as_finished/{disease_id}")
async def mark_disease_as_finished(
        disease_id: int,
        session: SessionDep,
        update_date: datetime = None):
    return await DiseasesService.mark_disease_as_finished(disease_id=disease_id,
                                                          session=session,
                                                          update_date=update_date)
