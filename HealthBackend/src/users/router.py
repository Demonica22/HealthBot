from fastapi import APIRouter, status, Request
from fastapi.responses import StreamingResponse
from sqlalchemy import select, update
from datetime import datetime

from src.database.session import SessionDep
from src.users.models import User
from src.users.schemas import UserSchema, UserPatchSchema
from src.diseases.schemas import DiseaseSchema
from src.diseases.enums import DiseasesResponseFormat, UserLanguage
from src.diseases.models import Disease
from src.utils.constants import STRING_DATE_FORMAT
from src.utils.make_diseases_document import make_in_memory_document
from src.utils.generate_html_page import get_diseases_template

router = APIRouter(prefix="/users")


@router.get("/")
async def get_all_users(session: SessionDep):
    query = select(User)
    result = await session.execute(query)
    users = result.scalars().all()
    return users


@router.post(path="/",
             response_model=UserSchema,
             status_code=status.HTTP_201_CREATED)
async def add_user(data: UserSchema, session: SessionDep):
    data = data.model_dump()
    new_user = User(
        id=data['id'],
        name=data['name'],
        gender=data['gender'],
        language=data['language'],
        weight=data['weight'],
        height=data['height'],
    )
    session.add(new_user)
    await session.commit()
    return new_user


@router.get("/{user_id}")
async def get_user(user_id: int, session: SessionDep):
    query = select(User).where(User.id == user_id)
    result = await session.execute(query)
    user = result.scalars().first()
    return user


@router.patch("/{user_id}")
async def update_user(user_id: int,
                      session: SessionDep,
                      body: UserPatchSchema):
    try:
        update_data = body.model_dump(exclude_none=True)
        query = update(User).where(User.id == user_id).values(**update_data)
        await session.execute(query)
    except Exception as ex:
        await session.rollback()
        return {"success": False, "message": ex}
    else:
        await session.commit()
        return {"success": True}


@router.get("/diseases/{user_id}")
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

    result = await session.execute(query)

    diseases = [DiseaseSchema.from_orm(disease).model_dump() for disease in result.scalars().all()]

    if response_format == "json":
        return diseases
    elif response_format == "docx":
        return StreamingResponse(content=make_in_memory_document(diseases, user_language),
                                 headers={'Content-Disposition': 'attachment; filename="diseases.docx"'})
    elif response_format == "html":
        return await get_diseases_template(diseases, user_language, request)
