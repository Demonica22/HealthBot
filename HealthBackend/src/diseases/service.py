import logging
from fastapi import Request

from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update
from datetime import datetime

from src.database.session import SessionDep
from src.diseases.models import Disease
from src.diseases.schemas import DiseaseSchemaAdd, DiseaseSchema
from src.diseases.enums import *
from src.users.models import User
from src.users.schemas import UserSchema
from src.utils.constants import STRING_DATE_FORMAT
from src.utils.make_diseases_document import make_in_memory_document
from src.utils.generate_html_page import get_diseases_template


class DiseasesService:

    @staticmethod
    async def add_disease(data: DiseaseSchemaAdd, db_session: SessionDep):
        data = data.model_dump()
        new_disease = Disease(
            **data
        )
        db_session.add(new_disease)
        await db_session.commit()

        return new_disease

    @staticmethod
    async def get_disease(disease_id: int, db_session: SessionDep):
        query = select(Disease).where(Disease.id == disease_id)
        result = await db_session.execute(query)
        disease = result.scalars().first()
        return disease

    @staticmethod
    async def get_all_user_diseases(user_id: int,
                                    session: SessionDep,
                                    request: Request,
                                    response_format: DiseasesResponseFormat,
                                    user_language: UserLanguage,
                                    start_date: str = "-1",
                                    only_active: bool = False):
        query = select(Disease).where(Disease.user_id == user_id)
        if only_active:
            query = query.where(Disease.still_sick == True)

        if start_date != "-1":
            start_date = datetime.strptime(start_date, STRING_DATE_FORMAT)
            query = query.where((Disease.date_to > start_date) | (Disease.still_sick == True))
        query = query.order_by(Disease.date_from)
        result = await session.execute(query)

        diseases = [DiseaseSchema.from_orm(disease).model_dump() for disease in result.scalars().all()]
        user_query = select(User).where(User.id == user_id)
        user_data = UserSchema.from_orm((await session.execute(user_query)).scalars().first()).model_dump()
        if response_format == "json":
            return diseases
        elif response_format == "docx":
            return StreamingResponse(content=make_in_memory_document(diseases, user_data, user_language),
                                     headers={'Content-Disposition': 'attachment; filename="diseases.docx"'})
        elif response_format == "html":
            return await get_diseases_template(diseases, user_data, user_language, request)

    @staticmethod
    async def mark_disease_as_finished(disease_id: int,
                                       session: SessionDep,
                                       update_date: datetime = None):
        try:
            if update_date is None:
                update_date = datetime.now()
            query = update(Disease).where(Disease.id == disease_id).values(still_sick=False, date_to=update_date)
            await session.execute(query)
        except Exception as ex:
            await session.rollback()
            return {"success": False, "message": ex}
        else:
            await session.commit()
            return {"success": True}
