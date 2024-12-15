from aiogram.fsm.state import State, StatesGroup


class UserChangeData(StatesGroup):
    field_name = State()
    new_data = State()
