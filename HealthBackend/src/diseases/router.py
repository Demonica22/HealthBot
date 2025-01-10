from fastapi import APIRouter, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update
from datetime import datetime

from src.database.session import SessionDep
from src.diseases.models import Disease
from src.diseases.schemas import DiseaseSchemaAdd, DiseaseSchema
from src.diseases.enums import DiseasesResponseFormat, UserLanguage
from src.utils.constants import STRING_DATE_FORMAT
from src.utils.make_diseases_document import make_in_memory_document
from src.utils.generate_html_page import get_diseases_template

router = APIRouter(prefix="/diseases", tags=['Diseases'])


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


@router.get("/for_user/{user_id}")
async def get_all_user_diseases(user_id: int,
                                session: SessionDep,
                                request: Request,
                                start_date: str = "-1",
                                response_format: DiseasesResponseFormat = DiseasesResponseFormat.json,
                                user_language: UserLanguage = UserLanguage.ru):
    query = select(Disease).where(Disease.user_id == user_id)

    if start_date != "-1":
        start_date = datetime.strptime(start_date, STRING_DATE_FORMAT)
        query = query.where((Disease.date_to > start_date) | (Disease.still_sick == True))
    query = query.order_by(Disease.date_from)
    result = await session.execute(query)

    diseases = [DiseaseSchema.from_orm(disease).model_dump() for disease in result.scalars().all()]

    if response_format == "json":
        return diseases
    elif response_format == "docx":
        return StreamingResponse(content=make_in_memory_document(diseases, user_language),
                                 headers={'Content-Disposition': 'attachment; filename="diseases.docx"'})
    elif response_format == "html":
        return await get_diseases_template(diseases, user_language, request)
