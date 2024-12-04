from aiogram.fsm.state import State, StatesGroup


class UserRegistration(StatesGroup):
    """FSM states for user registration."""
    name = State()
    gender = State()
    language = State()
    weight = State()
    height = State()
