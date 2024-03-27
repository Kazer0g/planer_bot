import asyncio
import logging
# TODO: Clean imports
# TODO: Format code
import src
import keyboards
import aiogram
import sqlite_db
from aiogram import Bot, Dispatcher, F, Router, exceptions
from aiogram.enums.parse_mode import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.fsm.context import FSMContext
from aiogram.client.bot import DefaultBotProperties
from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command
from datetime import datetime
from enums import BotMessages, Commands, Callbacks, States, DataNames
from sqlite_db import connect_db

router = Router()

# * Commands
@router.message(Command(commands=[Commands.start.value]))
async def start(msg: Message, state: FSMContext):
    sqlite_db.add_user(id=msg.from_user.id, username=msg.from_user.username, message_id = msg.message_id+1)
    await msg.answer(text=BotMessages.lists.value, reply_markup=keyboards.lists_menu(msg.from_user.id))
    await msg.delete()
    await state.set_state(States.lists)

# @router.message(Command(commands=[Commands.help.value]))
# async def help(msg: Message, state: FSMContext):
#     pass # TODO: Create help message
#     # await msg.answer(text=BotMessages.help.value)

# * Lists
@router.callback_query(F.data == Callbacks.add_new_list.value)
async def add_new_list(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(state=States.set_list_name)
    await clbck.bot.send_message(clbck.from_user.id, text=BotMessages.send_list_name.value)
@router.callback_query(F.data == Callbacks.delete_list.value)
async def delete_list(clbck: CallbackQuery, state: FSMContext):
    await clbck.bot.send_message(clbck.from_user.id, text=BotMessages.accept_deleting_list.value, reply_markup=keyboards.accept_deleting())
    await state.set_state(state=States.deleting_list)
@router.callback_query(States.deleting_list)
async def deleting_list(clbck: CallbackQuery, state: FSMContext):
    if clbck.data == Callbacks.accept.value:
        data = await state.get_data()
        sqlite_db.delete_list(int(data[DataNames.list_id.value]))
        await clbck.bot.delete_message(chat_id=clbck.from_user.id, message_id=clbck.message.message_id)
        await state.set_data([])
        await state.set_state(States.lists)
        await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), text=BotMessages.lists.value)
        await clbck.bot.edit_message_reply_markup(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), reply_markup=keyboards.lists_menu(clbck.from_user.id))
    elif clbck.data == Callbacks.cancel.value:
        await state.set_state(States.list)
        await clbck.bot.delete_message(chat_id=clbck.from_user.id, message_id=clbck.message.message_id)
@router.message(States.set_list_name)
async def set_list_name(msg: Message, state: FSMContext):
    await msg.bot.delete_messages(chat_id=msg.from_user.id, message_ids=[i for i in range(msg.message_id-1, msg.message_id+1)])
    sqlite_db.add_list(owner_id=msg.from_user.id, name=msg.text)
    await msg.bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), reply_markup=keyboards.lists_menu(msg.from_user.id)) 
    await state.set_state(state=States.lists)
@router.callback_query(States.lists)
async def lists(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(state=States.list)
    await state.set_data({DataNames.list_id.value: clbck.data})
    await clbck.bot.edit_message_text(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, text=sqlite_db.get_list_name(int(clbck.data)))
    await clbck.bot.edit_message_reply_markup(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, reply_markup=keyboards.list_menu(int(clbck.data))) # TODO: list markup
@router.callback_query(F.data == Callbacks.back_to_lists.value)
async def back_to_lists(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(state=States.lists)
    await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), text=BotMessages.lists.value)
    await clbck.bot.edit_message_reply_markup(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), reply_markup=keyboards.lists_menu(clbck.from_user.id))
@router.callback_query(F.data == Callbacks.add_new_task.value)
async def add_new_task(callback: CallbackQuery, state: FSMContext):
    data  = await state.get_data()
    await state.set_data({DataNames.list_id.value: data[DataNames.list_id.value]})
    await state.set_state(States.set_task_name)
    await callback.message.answer(text=BotMessages.set_task_name.value)
@router.callback_query(States.list)
async def tasks(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.task)
    data = await state.get_data()
    data[DataNames.task_id.value] = clbck.data
    await state.set_data({DataNames.task_id.value: clbck.data, DataNames.list_id.value: data[DataNames.list_id.value]})
    await clbck.bot.edit_message_text(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, text=sqlite_db.get_task_name(int(data[DataNames.task_id.value])))
    await clbck.bot.edit_message_reply_markup(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, reply_markup=keyboards.task_menu(int(data[DataNames.task_id.value])))

# * Tasks
@router.message(States.set_task_name)
async def set_task_name(msg: Message, state: FSMContext):
    data = await state.get_data()
    data[DataNames.name.value] = msg.text
    await state.set_data(data)
    await state.set_state(States.set_task_description)
    await msg.answer(text=BotMessages.set_task_description.value)
@router.message(States.set_task_description)
async def set_task_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    data[DataNames.description.value] = msg.text
    await state.set_data(data)
    await state.set_state(States.set_task_deadline)
    await msg.answer(text=BotMessages.set_task_deadline.value)
@router.message(States.set_task_deadline)
async def set_task_deadline(msg: Message, state: FSMContext):
    data = await state.get_data()
    if date_validator(msg.text):
        data[DataNames.deadline.value] = msg.text
        sqlite_db.add_task(owner_id=msg.from_user.id, list_id=data[DataNames.list_id.value], name=data[DataNames.name.value], description=data[DataNames.description.value], deadline=data[DataNames.deadline.value])
        await msg.bot.delete_messages(chat_id=msg.from_user.id, message_ids=[i for i in range(msg.message_id-5, msg.message_id+1)])
        await msg.bot.edit_message_text(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), text=sqlite_db.get_list_name(data[DataNames.list_id.value]))
        await msg.bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), reply_markup=keyboards.list_menu(data[DataNames.list_id.value]))
        await state.set_state(States.list)
        await state.set_data({DataNames.list_id.value: data[DataNames.list_id.value]})
    else:
        pass
@router.callback_query(F.data == Callbacks.back_to_list.value)
async def back_to_list(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data() 
    await state.set_state(States.list)
    await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), text=sqlite_db.get_list_name(data['list_id']))
    await clbck.bot.edit_message_reply_markup(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), reply_markup=keyboards.list_menu(data['list_id']))
@router.callback_query(F.data == Callbacks.description.value)
async def description(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.change_task_description)
    await clbck.bot.send_message(chat_id=clbck.from_user.id, text=BotMessages.set_task_description.value)
@router.message(States.change_task_description)
async def change_task_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    sqlite_db.update_task_description(id=data[DataNames.task_id.value], description=msg.text)
    await msg.bot.delete_messages(chat_id=msg.from_user.id, message_ids=[i for i in range(msg.message_id-1, msg.message_id+1)])
    await msg.bot.edit_message_text(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), text=sqlite_db.get_task_name(data[DataNames.task_id.value]))
    await msg.bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), reply_markup=keyboards.task_menu(data[DataNames.task_id.value]))
    await state.set_state(States.task)
@router.callback_query(F.data == Callbacks.deadline.value)
async def deadline(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(States.change_task_deadline)
    await clbck.bot.send_message(chat_id=clbck.from_user.id, text=BotMessages.set_task_deadline.value)
@router.message(States.change_task_deadline)
async def change_task_deadline(msg: Message, state: FSMContext):
    data = await state.get_data()
    sqlite_db.update_task_deadline(id=data[DataNames.task_id.value], deadline=msg.text)
    await msg.bot.delete_messages(chat_id=msg.from_user.id, message_ids=[i for i in range(msg.message_id-1, msg.message_id+1)])
    await msg.bot.edit_message_text(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), text=sqlite_db.get_task_name(data[DataNames.task_id.value]))
    await msg.bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), reply_markup=keyboards.task_menu(data[DataNames.task_id.value]))
    await state.set_state(States.task)
@router.callback_query(F.data == Callbacks.delete_task.value)
async def delete_task(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sqlite_db.delete_task(id=data[DataNames.task_id.value])
    await clbck.bot.edit_message_text(chat_id=clbck.from_user.id, message_id=clbck.message.message_id, text=sqlite_db.get_list_name(data[DataNames.list_id.value]))
    await clbck.bot.edit_message_reply_markup(chat_id=clbck.from_user.id, message_id=clbck.message.message_id, reply_markup=keyboards.list_menu(data[DataNames.list_id.value]))
    await state.set_state(States.list)
async def reminder(tasks):
    if len(tasks) == 0:
        pass
    else:
        print (tasks)
        for task in tasks:
            await bot.send_message(chat_id=task[1], text=task[3], reply_markup=keyboards.task(task[0], ))
def date_validator(date):
    return True
# TODO : date validator
async def check_time():
    return datetime.now()
async def checker():
    await asyncio.sleep(60 - datetime.now().time().second)
    logging.info('Timer started')
    while True:
        date_time = await check_time()
        time = date_time.strftime("%H:%M:%S")
        date = date_time.strftime("%d.%m.%Y")
        await reminder(sqlite_db.reminder(date, time))
        await asyncio.sleep(60)
async def main():
    global dp, bot
    connect_db()

    loop = asyncio.get_running_loop()
    loop.create_task(checker()) 

    bot = Bot(token=src.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.set_my_description(BotMessages.bot_description.value)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
