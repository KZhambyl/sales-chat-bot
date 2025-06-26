from aiogram.fsm.state import State, StatesGroup

class OfferStates(StatesGroup):
    waiting_for_services_description = State()
