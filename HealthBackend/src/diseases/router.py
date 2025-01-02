import datetime

from fastapi import APIRouter, Response, status
from src.database.session import SessionDep
from sqlalchemy import select, update
from src.diseases.models import Disease
from src.diseases.schemas import DiseaseSchemaAdd

router = APIRouter(prefix="/diseases")


@router.post("/",
             # response_model=DiseaseSchemaAdd,
             status_code=status.HTTP_201_CREATED)
async def add_disease(data: DiseaseSchemaAdd, session: SessionDep):
    data = data.model_dump()
    # data['date_from'] = datetime.datetime.strptime(data['date_from'], "%d.%m.%Y").date()
    # data['date_to'] = datetime.datetime.strptime(data['date_to'], "%d.%m.%Y").date()
    new_disease = Disease(
        **data
    )
    session.add(new_disease)
    await session.commit()
    return new_disease
