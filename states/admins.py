from aiogram.dispatcher.filters.state import StatesGroup, State


class Rass(StatesGroup):
    post = State()
    kb = State()
    time = State()


class ABD(StatesGroup):
    start = State()
    step_1 = State()
    step_2 = State()
