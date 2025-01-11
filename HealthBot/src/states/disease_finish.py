from aiogram.fsm.state import State, StatesGroup


class DiseaseFinish(StatesGroup):
    disease_id = State()
