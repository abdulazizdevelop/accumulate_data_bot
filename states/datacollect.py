
from aiogram.dispatcher.filters.state import State, StatesGroup


#  states
class Data(StatesGroup):
    tech = State()         # Technology
    telegram = State()     # Telegram username
    contact = State()      # Contact information
    region = State()       # Region
    responsible = State()  # Responsible person
    work_time = State()    # Work time
    salary = State()       # Salary
    confirm = State()      # Confirmation
    
    
class FillGoogleFormState(StatesGroup):
    
    salary = State()
    name = State()
    age = State()
    region = State()       # Region
    confirm = State()



