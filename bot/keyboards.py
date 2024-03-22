from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
import sqlite_db
from enums import Callbacks, ButtonsText

# * InlineKeyboards
def lists_menu(owner_id) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text=ButtonsText.add_new_list.value, callback_data=Callbacks.add_new_list.value)],
        [InlineKeyboardButton(text=ButtonsText.all_tasks.value, callback_data=Callbacks.all_tasks_list.value)]
        ]
    for list in sqlite_db.get_lists_ids(owner_id):
        inline_keyboard.append(
            [InlineKeyboardButton(text=sqlite_db.get_list_name(list[0]), callback_data=str(list[0]))]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def list_menu(list_id) -> InlineKeyboardMarkup:
    inline_keyboard = [
        [InlineKeyboardButton(text='Удалить список', callback_data=Callbacks.delete_list.value)],
        [InlineKeyboardButton(text='Добавить задачу', callback_data=Callbacks.add_new_task.value)]
    ]
    tasks = sqlite_db.get_tasks(list_id)
    for task in tasks:
        print (task)
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def task_menu(task_id):
    task = sqlite_db.get_task(task_id)
    # TODO: Create task menu
    
