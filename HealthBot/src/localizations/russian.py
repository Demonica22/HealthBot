localization = {
    "system_clear_keyboard": "Очищаю клавиатуру...",
    "unexpected_error": "Непредвиденная ошибка: {}",
    "not_supported_message": "Извините, я не поддерживаю такое(",
    # РЕГИСТРАЦИЯ
    "greet_message": "Привет, {}!",
    "language_message": "Выберите ваш язык:",
    "name_message": "Введите ваше имя и фамилию:",
    "gender_message": "Выберите ваш пол:",
    "gender_list": ["Мужчина", "Женщина"],
    "weight_message": "Введите ваш вес:",
    "weight_error_message": "Укажите вес в формате числа!",
    "height_message": "Введите ваш рост в сантиметрах (пр. 160):",
    "height_error_message": "Укажите рост в формате числа!",
    "register_complete_message": "Регистрация завершена!",

    # Персональные данные
    "change_data_message": "Изменить свои данные",
    "name_field": "Имя",
    "gender_field": "Пол",
    "weight_field": "Вес",
    "height_field": "Рост",
    "language_field": "Язык",
    "user_info_message": "Ваше имя: {name}\n"
                         "Ваш пол: {gender}\n"
                         "Ваш язык: {language}\n"
                         "Ваш вес: {weight}\n"
                         "Ваш рост: {height}\n",
    "user_info_current_diseases_message": "Ваши болезни: {diseases}",
    "user_info_current_status_message": "Вы здоровы!",
    "change_info_message": "Выберите поле, которое хотите поменять:",
    "enter_new_data_for_change_message": "Введите новые данные для поля <b>{}</b>",
    "user_change_data_success_message": "Данные успешно обновлены!",
    # КНОПКИ
    "main_menu_message": "Главное меню",
    "back_button": "Назад",
    "to_main_menu_button": "В главное меню",
    "add_disease_button": "Добавить болезнь",
    "get_diseases_button": "Все болезни",
    "get_active_diseases_button": "Текущие болезни",
    "check_personal_data_button": "Свои данные",
    "mark_disease_as_finished": "Завершить болезнь",
    "yes": "Да",
    "no": "Нет",

    # БОЛЕЗНИ
    "add_disease_message": "Чем вы болеете?",
    "disease_description_message": "Опишите вашу болезнь (симптомы, осложнения, все что полезно врачу)",
    "disease_treatment_plan_message": "Если у вас есть план лечения напишите его:",
    "disease_date_start_message": "Когда заболели? (введите в формате ДД.ММ.ГГГГ)",
    "disease_date_end_message": "Когда выздоровели? (введите в формате ДД.ММ.ГГГГ)",
    "disease_incorrect_date": "Вы ввели дату в неверном формате, пожалуйста, введите в формате ДД.ММ.ГГГГ - 21.10.2024",
    "disease_still_sick_message": "До сих пор болеете?",
    "disease_add_success_message": "Болезнь успешно добавлена!",
    "disease_choose_inline_tip": "Введите свою болезнь или выберите из списка",
    "default_diseases_list": ["ОРВИ", "Грипп", "Аллергия", "Перелом", "Сердечно сосудистые заболевания"],

    "disease_date_choose_inline_tip": "Введите дату или выберите из списка",
    "disease_today_date_word": "Сегодня",
    "disease_yesterday_date_word": "Вчера",

    "get_diseases_message": "<b>Вот список всех ваших болезней:</b>\n",
    "get_active_diseases_message": "<b>Вот список ваших активных болезней:</b>\n",
    "get_diseases_empty_message": "Я не знаю ни одной вашей болезни!\nВы здоровы!",
    "diseases_filename": "Болезни.docx",
    "diseases_list_title": "Название",
    "diseases_list_description": "Описание",
    "diseases_list_treatment_plan": "План лечения",
    "diseases_list_start_date": "Дата заболевания",
    "diseases_list_end_date": "Дата выздоровления",
    "diseases_list_still_sick": "До сих пор болеете?",
    "diseases_list_total_days_sick": "Длительность болезни",

    "choose_diseases_periods_message": "За какое время вы хотите получить историю болезни?",
    "diseases_choose_how_to_get_message": "Как вы хотите получить список болезней?",
    "diseases_list_message_type": [("HTML страница", "html"), ("Сообщение в телеграмм", "telegram"),
                                   ("Word Таблица", "word")],
    "diseases_page_message": "Вот таблица с вашими болезнями",

    "diseases_choose_to_finish": "Выберите какая из болезней закончилась:\n",
    "diseases_finished_message": "Болезнь <b>{}</b> помечена как оконченная",
    # название для кнопки + длительность периода в месяцах.
    "diseases_list_of_periods": [("1 месяц", 1),
                                 ("3 месяца", 3),
                                 ("6 месяцев", 6),
                                 ("Год", 12),
                                 ("Все время", -1)],

    # Уведомления
    "make_medicine_notification_button": "Добавить прием лекарств",
    "make_doctor_notification_button": "Добавить прием врача",
    "notifications_main_menu_message": "Выберите действие:",
    "notifications_chose_medicine_message": "Введите название лекарства для приема:",
    "notifications_duration_inline_tip": "Выберите из предложенного списка или введите число дней:\n",
    "notifications_duration_message": "Сколько дней вам нужно принимать лекарства?\n",
    "notifications_default_duration_list": ["3", "5", "7", "10", "14"],
    "notifications_duration_type_error": "Введите длительность приема лекарств числом!",
    "notifications_times_a_day_list": ["1", "2", "3", "4"],
    "notifications_times_a_day_inline_tip": "Выберите из предложенного списка или введите число:\n",
    "notifications_times_a_day_message": "Выберите сколько раз в день вам нужно принимать лекарства:",
    "notifications_times_a_day_type_error": "Введите количество приемов в день числом!",

    "notifications_choose_time_message": "Введите время для приема №{}:",
    "notifications_time_format_error": "Время следует вводить в формате ЧЧ:ММ!",
    "notifications_time_increase_error": "Приемы нужно вводить по возрастанию, то есть "
                                         "каждый следующий прием должен быть позже предыдущего!",
    "notifications_add_successful_message": "Уведомление о приеме лекарства {medicine_name}\n"
                                            "длительностью {duration},\n"
                                            "в {times}\n"
                                            "успешно добавлено!",
    "notifications_get_all_button": "Посмотреть свои уведомления",
    "notifications_medicine_name_label": "Название лекарства",
    "notifications_end_date_label": "Уведомлять до",
    "notifications_in_label": "В ",
    "notifications_delete_button": "Удалить уведомления",
    "notifications_message": "Вам нужно принять лекарство: {}",
    "notifications_choose_to_delete": "Выберите какое уведомление вы хотите удалить:\n",
    "notification_deleted_message": "Уведомление успешно удалено!",
    "notifications_empty_list":"У вас пока нет уведомлений",
    "day_word": "день",
    "what_is_next": "Что делаем дальше?",

}
