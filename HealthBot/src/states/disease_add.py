from aiogram.fsm.state import State, StatesGroup


class DiseaseAdd(StatesGroup):
    title = State()
    description = State()
    treatment_plan = State()
    date_from = State()
    still_sick = State()
    date_to = State()
    for_patient = State()
