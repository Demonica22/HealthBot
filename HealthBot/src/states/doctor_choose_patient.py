from aiogram.fsm.state import State, StatesGroup


class FreePatientChoose(StatesGroup):
    patient_id = State()


class DoctorsPatientChoose(StatesGroup):
    patient_id = State()
    action = State()