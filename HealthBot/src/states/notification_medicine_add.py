from aiogram.fsm.state import State, StatesGroup


class MedicineNotificationAdd(StatesGroup):
    medicine_name = State()
    duration = State()
    times_a_day = State()
    time_notifications = State()
