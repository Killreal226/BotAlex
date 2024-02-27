from aiogram.fsm.state import State, StatesGroup


class BoardSelectorStates(StatesGroup):
    name = State()
    experience = State()
    riding_style = State()
    purpose = State()
    preferences = State()
