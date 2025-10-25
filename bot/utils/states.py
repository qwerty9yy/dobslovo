from aiogram.fsm.state import State, StatesGroup

class NewsPapers(StatesGroup):
    newspapers = State()
    
class AdminState(StatesGroup):
    newsletter = State()
    add_and_change_calendars = State()
    edit_newspapers_photo = State()
    
class SupportState(StatesGroup):
    waiting_for_question = State()
    
class Bible(StatesGroup):
    bible_search = State()