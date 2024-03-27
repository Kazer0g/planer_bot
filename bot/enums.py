from enum import Enum
from aiogram.fsm.state import State, StatesGroup

# TODO: Rewtrite statements

class ButtonsText(Enum):
    add_new_list = 'Добавить список ✅'
    delete_list = 'Удалить список ❌'

    add_new_task = 'Добавить задачу ✅'
    all_tasks = 'Все задачи'

    done = 'Выполнено ✔️'
    reschedule = 'Перенести '

    yes = 'Да'
    no = 'Нет'

    back = 'Назад ⬅'

class BotMessages(Enum):
    bot_description = 'My name is margo...' # TODO: Add description

    set_task_name = 'Введите задачу'
    set_task_description = 'Введите описание задачи'
    set_task_deadline = 'Введите дедлайн задачи DD.MM.YYYY hh.mm.ss'

    lists = 'Списки задач 📋'
    send_list_name = 'Введите название списка'
    accept_deleting_list = 'Вы уверены, что хотите удалить список? Все задачи в этом списке будут удалены!'

class Commands(Enum):
    start = 'start'
    task = 'task'
    home = 'home'

class Callbacks(Enum):
    add_new_task = 'add_task'
    task = 'task'

    done = 'done'
    reschedule = 'reschedule'

    back_to_list = 'back_to_list'
    back_to_lists = 'back_to_lists'

    add_new_list = 'add_new_list'
    delete_list = 'delete_list'
    all_tasks_list = 'all_tasks_list'

    accept = 'accept'
    cancel = 'cancel'
    
class DataNames(Enum):
    list_id = 'list_id'
    task_id = 'task_id'
    name = 'name'
    description = 'description'
    deadline = 'deadline'

class States(StatesGroup):
    set_task_name = State()
    set_task_description = State()
    set_task_deadline = State()
    task = State()

    lists = State()
    list = State()
    set_list_name = State()
    deleting_list = State()


