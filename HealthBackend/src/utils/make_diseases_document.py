import docx
from docx.shared import Pt
from io import BytesIO

messages = {
    "ru": {
        "table_title": "Таблица Болезней",

        "title": "Заголовок",
        "description": "Описание",
        "treatment_plan": "План лечения",
        "date_from": "Дата заболевания",
        "date_to": "Дата выздоровления",
        "still_sick": "До сих пор больны?",

        "no": "Нет",
        "yes": "Да",
    },
    "en": {
        "table_title": "Illness Table",

        "title": "Title",
        "description": "Description",
        "treatment_plan": "Treatment Plan",
        "date_from": "Date From",
        "date_to": "Date To",
        "still_sick": "Still Sick?",

        "no": "No",
        "yes": "Yes",
    }
}


def make_in_memory_document(diseases: list[dict], user_language: str):
    doc = docx.Document()
    doc.add_heading(messages[user_language]['table_title'], level=1)
    headers = [messages[user_language]['title'],
               messages[user_language]['description'],
               messages[user_language]['treatment_plan'],
               messages[user_language]['date_from'],
               messages[user_language]['date_to'],
               messages[user_language]['still_sick'], ]
    table = doc.add_table(rows=1, cols=len(headers), style='Table Grid')
    table.autofit = True
    header_cells = table.rows[0].cells
    for i, header in enumerate(headers):
        header_cells[i].text = header
    for illness in diseases:
        row_cells = table.add_row().cells
        row_cells[0].text = illness["title"]
        row_cells[1].text = illness["description"]
        row_cells[2].text = illness["treatment_plan"]
        row_cells[3].text = illness["date_from"].strftime("%Y-%m-%d")
        row_cells[4].text = illness["date_to"].strftime("%Y-%m-%d") if illness["date_to"] else "-"
        row_cells[5].text = messages[user_language]['yes'] if illness["still_sick"] else messages[user_language]['no']

    # Save the document to memory
    memory_stream = BytesIO()
    doc.save(memory_stream)
    memory_stream.seek(0)

    return memory_stream
