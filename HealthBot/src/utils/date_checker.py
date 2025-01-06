import datetime

from src.localizations import get_text


def check_message_for_date(message_text: str,
                           user_language: str) -> str | None:
    """
    Проверяет message_text на равенство одной из дат today|yesterday и возвращает дату в стандартном формате.
    Иначе возвращает None
    """
    today = get_text("disease_today_date_word", lang=user_language).lower()
    yesterday = get_text("disease_yesterday_date_word", lang=user_language).lower()
    possible_word_dates = (today, yesterday)
    date = None
    if message_text in possible_word_dates:
        if message_text == today:
            date = datetime.datetime.today().strftime("%d.%m.%Y")
        elif message_text == yesterday:
            date = (datetime.datetime.today() - datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    return date
