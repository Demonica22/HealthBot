from aiogram.fsm.state import State, StatesGroup


class DiseaseRequest(StatesGroup):
    how_long = State()
    how = State()
