from aiogram.fsm.state import State, StatesGroup


class DoctorAddAppointment(StatesGroup):
    patient_id = State()
    date = State()
    time = State()
    notify_your_self = State()
