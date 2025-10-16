from aiogram.fsm.state import State, StatesGroup

class NewsPapers(StatesGroup):
    newspapers = State()
    
class AdminState(StatesGroup):
    newsletter = State()