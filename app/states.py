from aiogram.fsm.state import State, StatesGroup

class ReflectionWizard(StatesGroup):
    mood = State()
    text = State()
    tags = State()
