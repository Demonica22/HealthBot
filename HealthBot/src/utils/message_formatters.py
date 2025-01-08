from src.localizations import get_text

def generate_diseases_message(diseases: list[dict],
                              user_language: str) -> str:
    if user_language == "ru":
        from pymorphy3 import MorphAnalyzer
        morph = MorphAnalyzer(lang=user_language)
    message = "--------------------\n"
    for disease in diseases:
        message += (
            f"<b>{get_text("diseases_list_title", user_language)}:</b>\n{disease['title']}\n"
            f"<b>{get_text("diseases_list_description", user_language)}:</b>\n{disease['description']}\n"
            f"<b>{get_text("diseases_list_treatment_plan", user_language)}:</b>\n{disease['treatment_plan'] if disease['treatment_plan'] else "-"}\n"
            f"<b>{get_text("diseases_list_start_date", user_language)}:</b>\n{disease['date_from']}\n"
        )
        if disease['date_to']:
            message += f"<b>{get_text("diseases_list_end_date", user_language)}:</b>\n{disease['date_to']}\n"
            sick_days = (disease['date_to'] - disease['date_from']).days
            days_word = get_text("day_word", user_language)
            if user_language == "ru":
                days_word = morph.parse(days_word)[0].make_agree_with_number(sick_days).word

            message += (f"<b>{get_text("diseases_list_total_days_sick", user_language)}:</b>\n{sick_days} "
                        f"{days_word}\n")
        else:
            message += f"<b>{get_text("diseases_list_still_sick", user_language)}:</b>\n{get_text("yes", user_language)}\n"
        message += f"\n--------------------\n"
    return message
