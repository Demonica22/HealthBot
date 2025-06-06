localization = {
    "system_clear_keyboard": "Clearing keyboards...",
    "unexpected_error": "Unexpected error: {}",
    "not_supported_message": "Sorry, I don't support this(",

    # REGISTRATION
    "greet_message": "Hello, {}!",
    "language_message": "Select your language:",
    "name_message": "Enter your first and last name:",
    "gender_message": "Select your gender:",
    "gender_list": ["Male", "Female"],
    "weight_message": "Enter your weight:",
    "weight_error_message": "Specify the weight in number format!",
    "weight_overflow_error_message": "The weight should be lower than: {}!",
    "height_message": "Enter your height in centimeters (e.g., 160):",
    "height_error_message": "Specify the height in number format!",
    "height_overflow_error_message": "The height should be lower than: {}!",
    "register_complete_message": "Registration complete!",
    "only_button_input_allowed_message": "You should use button to input new value for the selected field!",

    # Personal Data
    "change_data_message": "Edit your information",
    "name_field": "Name",
    "gender_field": "Gender",
    "weight_field": "Weight",
    "height_field": "Height",
    "language_field": "Language",
    "user_info_message": "Your name: {name}\n"
                         "Your gender: {gender}\n"
                         "Your language: {language}\n"
                         "Your weight: {weight}\n"
                         "Your Height: {height}\n",
    "user_info_current_diseases_message": "Current diseases: {diseases}",
    "user_info_current_status_message": "You are Healthy!",
    "change_info_message": "Select the field you want to change:",
    "enter_new_data_for_change_message": "Enter new data for the field <b>{}</b>",
    "user_change_data_success_message": "The data has been updated successfully!",

    # BUTTONS
    "main_menu_message": "Main Menu",
    "back_button": "Back",
    "to_main_menu_button": "To Main Menu",
    "add_disease_button": "Add a disease",
    "get_diseases_button": "All diseases",
    "get_active_diseases_button": "Active diseases",
    "check_personal_data_button": "Your information",
    "mark_disease_as_finished": "Finish a disease",

    "yes": "Yes",
    "no": "No",

    # DISEASES
    "add_disease_message": "Enter the name of the disease",
    "disease_description_message": "Describe the symptoms and complications",
    "disease_treatment_plan_message": "Describe the treatment plan (if applicable)",
    "disease_date_start_message": "Enter the start date of the disease (format: DD.MM.YYYY)",
    "disease_date_end_message": "Enter the end date of the disease (format: DD.MM.YYYY)",
    "disease_still_sick_message": "Has the disease ended?",
    "incorrect_date_message": "You entered the date in an incorrect format, please enter in the format DD.MM.YYYY - 21.10.2024",
    "disease_add_success_message": "Disease successfully added!",
    "disease_choose_inline_tip": "Enter your disease or select from the list",
    "default_diseases_list": ["SARS", "Flu", "Allergy", "Fracture", "Сardiovascular diseases"],

    "disease_date_choose_inline_tip": "Enter the date or select from the list",
    "disease_today_date_word": "Today",
    "disease_yesterday_date_word": "Yesterday",

    "get_diseases_message": "<b>Here is a list of all your diseases:</b>\n",
    "get_active_diseases_message": "<b>Here is a list of your active diseases:</b>\n",
    "diseases_filename": "Diseases.docx",
    "get_diseases_empty_message": "I don't know any of your illnesses!\nYou are healthy!",
    "diseases_list_title": "Title",
    "diseases_list_description": "Description",
    "diseases_list_treatment_plan": "Treatment plan",
    "diseases_list_start_date": "Date of illness",
    "diseases_list_end_date": "Date of recovery",
    "diseases_list_still_sick": "Still sick?",
    "diseases_list_total_days_sick": "Illness duration",

    "choose_diseases_periods_message": "How far back do you wish to trace your medical history?",
    "diseases_choose_how_to_get_message": "How do you want to get a list of diseases?",
    "diseases_list_message_type": [("HTML page", "html"), ("Message in Telegram", "telegram"),
                                   ("Word table", "word")],
    "diseases_page_message": "Here is your diseases page",
    "diseases_choose_to_finish": "Choose disease to finish:\n",
    "diseases_finished_message": "Disease <b>{}</b> was marked as finished",
    # название для кнопки + длительность периода в месяцах.
    "diseases_list_of_periods": [("1 month", 1),
                                 ("3 months", 3),
                                 ("6 months", 6),
                                 ("1 year", 12),
                                 ("All Time", -1)],

    "notifications_main_menu_button": "Notifications",
    "make_medicine_notification_button": "Add medicine intake",
    "make_doctor_notification_button": "Add doctor appointment",
    "notifications_main_menu_message": "Choose an action:",
    "notifications_chose_medicine_message": "Enter the name of the medicine to take:",
    "notifications_duration_inline_tip": "Choose from the suggested list or enter the number of days:\n",
    "notifications_duration_message": "How many days do you need to take the medicine?\n",
    "notifications_default_duration_list": ["3", "5", "7", "10", "14"],
    "notifications_duration_type_error": "Please enter the duration of medicine intake as a number!",
    "notifications_times_a_day_validation_error": "The duration should be greater than zero!",
    "notifications_times_a_day_list": ["1", "2", "3", "4"],
    "notifications_times_a_day_inline_tip": "Choose from the suggested list or enter the number:\n",
    "notifications_times_a_day_message": "Choose how many times a day you need to take the medicine:\n",
    "notifications_times_a_day_type_error": "Please enter the number of doses per day as a number!",

    "notifications_choose_time_message": "Enter the time for intake №{}:",
    "time_format_error": "Time should be entered in the format HH:MM!",
    "notifications_time_increase_error": "Intakes must be entered in ascending order, meaning "
                                         "each subsequent intake should be later than the previous one!",
    "notifications_add_successful_message": "Notification for medicine intake {medicine_name}\n"
                                            "at {times}\n"
                                            "until {duration},\n"
                                            "successfully added!",
    "notifications_get_all_button": "View your notifications",
    "notifications_medicine_name_label": "Medicine name",
    "notifications_end_date_label": "Notify until",
    "notifications_start_date_label": "Notify from",
    "notifications_in_label": "In ",
    "notifications_delete_button": "Delete notifications",
    "notifications_message": "You need to take the medicine: {}",
    "notifications_choose_to_delete": "Choose which notification you want to delete:\n",
    "notification_deleted_message": "Notification successfully deleted!",
    "notifications_empty_list": "You don't have any notifications yet",

    "notifications_add_error": "Error adding notification: {}",
    "doctor_get_patients_button": "List of your patients",
    "get_doctor_schedule_button": "Appointment schedule",

    "doctor_get_free_patients_button": "List of available patients",
    "doctor_menu_button": "To doctor’s menu",
    "doctor_menu": "Doctor’s menu",
    "users_free_empty_list_message": "No available patients found.",
    "users_mine_empty_list_message": "You don't have any patients yet.",
    "current_diseases": "Current diseases",
    "user_is_healthy": "Healthy",
    "drop_patient_button": "Drop patient",
    "doctor_choose_patient_button": "Choose a patient",
    "patient_choose_success_message": "Patient {} has been assigned to you",
    "sure_to_drop_patient_message": "Are you sure you want to drop patient {}?",
    "patient_drop_success_message": "You have dropped patient {}",
    "choose_patient_message": "Select a patient:",
    "patient_actions_message": "You are viewing patient: {}\nSelect the action you want to perform:",
    "add_disease_for_patient_button": "Register disease",
    "end_disease_for_patient_button": "End disease",
    "add_appointment_for_patient_button": "Schedule an appointment",
    "get_patient_medical_card_button": "View patient’s medical record",
    "get_patient_medical_card_message": "Here is your patient’s medical record:",
    "appointment_date_message": "Enter the appointment date (in the format DD.MM.YYYY)",
    "appointment_time_message": "Enter the appointment time (in the format HH:MM)",
    "appointment_notify_your_self_message": "Would you like to be notified about this appointment?",
    "appointment_add_success_message": "Appointment notification successfully added!",
    "appointment_notification_for_patient_message": "You have a scheduled appointment with doctor {} {} at {}",
    "appointment_notification_for_doctor_message": "You have a scheduled appointment with patient {} {} at {}",
    "doctor_appointments_empty_list_message": "You dont have any appointments yet.",

    "back_to_patient_menu_button": "Back to patient menu",

    "day_word": "days",
    "what_is_next": "What is next?",

}
