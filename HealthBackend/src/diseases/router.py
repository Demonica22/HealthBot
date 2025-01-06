from fastapi import APIRouter, Response, status
from src.database.session import SessionDep
from src.diseases.models import Disease
from src.diseases.schemas import DiseaseSchemaAdd, DiseaseSchema

router = APIRouter(prefix="/diseases")


@router.post("/",
             response_model=DiseaseSchema,
             status_code=status.HTTP_201_CREATED)
async def add_disease(data: DiseaseSchemaAdd, session: SessionDep):
    data = data.model_dump()
    new_disease = Disease(
        **data
    )
    session.add(new_disease)
    await session.commit()

    return new_disease
