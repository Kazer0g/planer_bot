from enum import Enum
from aiogram.fsm.state import State, StatesGroup

class ButtonsText(Enum):
    add_new_list = 'Добавить список'
    all_tasks = 'Все задачи'

class BotMessages(Enum):
    bot_description = 'My name is margo...'

    lists = 'Списки задач'
    send_list_name = 'Введите название списка'

class Commands(Enum):
    start = 'start'

class Callbacks(Enum):
    add_new_task = 'add_task'
    task = 'task'

    add_new_list = 'add_new_list'
    all_tasks_list = 'all_tasks_list'

class States(StatesGroup):
    set_task_name = State()
    set_task_description = State()

    set_list_name = State()
