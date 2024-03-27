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
        [InlineKeyboardButton(text=ButtonsText.back.value, callback_data=Callbacks.back_to_lists.value)],
        [InlineKeyboardButton(text=ButtonsText.delete_list.value, callback_data=Callbacks.delete_list.value)],
        [InlineKeyboardButton(text=ButtonsText.add_new_task.value, callback_data=Callbacks.add_new_task.value)]
    ]
    tasks = list(sorted(sqlite_db.get_tasks(list_id), key=lambda x: x[5]))
    for task in tasks:
        inline_keyboard.append(
            [InlineKeyboardButton(text=task[5], callback_data=str(task[0])),
             InlineKeyboardButton(text=task[3], callback_data=str(task[0]))]
        )
    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)

def task_menu(task_id) -> InlineKeyboardMarkup:
    task = sqlite_db.get_task(task_id)
    inlinekeyboard = [
        [InlineKeyboardButton(text=ButtonsText.back.value, callback_data=Callbacks.back_to_list.value)],
        # [InlineKeyboardButton(text=ButtonsText.edit_task.value, callback_data=Callbacks.edit_task.value),
        [InlineKeyboardButton(text=ButtonsText.delete_task.value, callback_data=Callbacks.delete_task.value)],
        [InlineKeyboardButton(text=task[5], callback_data=Callbacks.deadline.value)],
        [InlineKeyboardButton(text=task[4], callback_data=Callbacks.description.value)]
    ]   

    return InlineKeyboardMarkup(inline_keyboard=inlinekeyboard) 

def task(task_id) -> InlineKeyboardMarkup:
    task = sqlite_db.get_task(task_id)
    inlinekeyboard = [
        [InlineKeyboardButton(text=ButtonsText.done.value, callback_data=Callbacks.done.value),
         InlineKeyboardButton(text=ButtonsText.reschedule.value, callback_data=Callbacks.reschedule.value)],
    ]   

    return InlineKeyboardMarkup(inline_keyboard=inlinekeyboard)

def accept_deleting() -> InlineKeyboardMarkup:
    inlinekeyboard=[
        [InlineKeyboardButton(text=ButtonsText.yes.value, callback_data=Callbacks.accept.value),
         InlineKeyboardButton(text=ButtonsText.no.value, callback_data=Callbacks.cancel.value)],
    ]
    return InlineKeyboardMarkup(inline_keyboard=inlinekeyboard)