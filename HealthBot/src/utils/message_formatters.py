import datetime
def generate_telegram_message(diseases: list[dict]) -> str:
    message = ""
    for disease in diseases:
        message += (
            f"Название: {disease['title']}\n"
            f"Описание: {disease['description']}\n"
            f"План лечения: {disease['treatment_plan'] if disease['treatment_plan'] else "-"}\n"
            f"Дата начала: {disease['date_from']}\n"
        )
        message += f"Дата выздоровления: {disease['date_to']}\n" if disease['date_to'] \
            else f"До сих пор болеете?: {'Да'}\n"
        message += f"\n--------------------\n"
    return message
