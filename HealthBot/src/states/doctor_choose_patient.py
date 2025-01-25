from aiogram.fsm.state import State, StatesGroup


class PatientChoose(StatesGroup):
    patient_id = State()
