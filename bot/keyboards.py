from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
import sqlite_db
from enums import Callbacks
import json

def main_menu(owner_id):
    tasks = sqlite_db.get_tasks(owner_id)
    inline_keyboard = [[InlineKeyboardButton(text='Добавить задачу', callback_data=Callbacks.add_new_task.value)]]
    for task in tasks:
        inline_keyboard.append([InlineKeyboardButton(text=task, callback_data=json.dumps({Callbacks.task.value: tasks.index(task)}))])
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)


def task_menu(task_id):
    task = sqlite_db.get_task(task_id)
    
