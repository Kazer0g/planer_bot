from enum import Enum
from aiogram.fsm.state import State, StatesGroup

class ButtonsText(Enum):
    pass

class BotMessages(Enum):
    bot_description = 'My name is margo...'

class Commands(Enum):
    start = 'start'

class Callbacks(Enum):
    add_new_task = 'add_task'
    task = 'task'

class States(StatesGroup):
    set_task_name = State()
    set_task_description = State()

