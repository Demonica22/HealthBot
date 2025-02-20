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


def generate_active_diseases_message(diseases: list[dict],
                                     user_language: str) -> str:
    message = "--------------------\n"
    for i, disease in enumerate(diseases):
        message += (
            f"<b>№{i + 1}</b>\n"
            f"<b>{get_text("diseases_list_title", user_language)}:</b>\n{disease['title']}\n"
            f"<b>{get_text("diseases_list_start_date", user_language)}:</b>\n{disease['date_from']}\n"
        )
        message += f"\n--------------------\n"
    return message


def generate_notifications_message(notifications: list[dict], user_language: str) -> str:
    if not notifications:
        return get_text("notifications_empty_list", user_language)
    message = "--------------------\n"
    for i, notification in enumerate(notifications):
        message += f"({i + 1}) <b>{notification['message']}</b>\n"
        if notification['start_date']:
            message += f"<b>{get_text("notifications_start_date_label", user_language)}:</b>\n{notification['end_date']}\n"
        message += f"<b>{get_text("notifications_end_date_label", user_language)}:</b>\n{notification['end_date']}\n"

        message += get_text("notifications_in_label", user_language)
        for time in notification['time_notifications']:
            message += f"{time['time']} "
        message += "\n"
        message += f"\n--------------------\n"
    return message


def generate_users_message(users: list[dict], user_language: str, users_type: str) -> str:
    if not users:
        if users_type == "free":
            return get_text("users_free_empty_list_message", user_language)
        elif users_type == "mine":
            return get_text("users_mine_empty_list_message", user_language)
    message = "--------------------\n"
    for user in users:
        message += (
            f"<b>{get_text("name_field", user_language)}:</b>\n{user['name']}\n"
            f"<b>{get_text("gender_field", user_language)}:</b>\n{user['gender']}\n"
        )
        active_diseases = list(filter(lambda x: x['still_sick'], user['diseases']))
        if active_diseases:
            message += (f"<b>{get_text("current_diseases", user_language)}:</b>\n"
                        f"{','.join([d['title'] for d in active_diseases])}")
        else:
            message += f"<b>{get_text('user_is_healthy', user_language)}</b>"
        message += "\n"
        message += f"\n--------------------\n"
    return message


def generate_schedule_message(appointments: list[dict], user_language: str) -> str:
    if not appointments:
        return get_text("doctor_appointments_empty_list_message", user_language)

    message = "--------------------\n"
    for appointment in appointments:
        message += (
            f"<b>{appointment['message']}</b>\n"
        )
        message += f"\n--------------------\n"

    return message
