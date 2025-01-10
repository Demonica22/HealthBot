from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from src.utils.localization import constraints


async def get_diseases_template(diseases: list[dict], user_language: str, request) -> HTMLResponse:
    templates = Jinja2Templates(directory='src/templates')
    data = {
        "diseases": diseases,
        "table_name": constraints[user_language]['table_title'],
        "title": constraints[user_language]['title'],
        "description": constraints[user_language]['description'],
        "treatment_plan": constraints[user_language]['treatment_plan'],
        "date_from": constraints[user_language]['date_from'],
        "date_to": constraints[user_language]['date_to'],
        "still_sick": constraints[user_language]['still_sick'],
        "yes": constraints[user_language]['yes'],
        "no": constraints[user_language]['no']
    }
    return templates.TemplateResponse(name='diseases_table.html', request=request, context=data)
