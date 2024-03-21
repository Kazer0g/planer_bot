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
from enums import BotMessages, Commands, Callbacks, States
from sqlite_db import connect_db

router = Router()

@router.message(Command(commands=[Commands.start.value]))
async def start(msg: Message, state: FSMContext):
    sqlite_db.add_user(id=msg.from_user.id, username=msg.from_user.username, message_id = msg.message_id+1)
    await state.set_state(States.lists)
    await msg.answer(text=BotMessages.lists.value, reply_markup=keyboards.lists_menu(msg.from_user.id))
    await msg.delete()

# * Lists
@router.callback_query(F.data == Callbacks.add_new_list.value)
async def add_new_list(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(state=States.set_list_name)
    await clbck.bot.send_message(clbck.from_user.id, text=BotMessages.send_list_name.value)
@router.message(States.set_list_name)
async def set_list_name(msg: Message, state: FSMContext):
    await msg.bot.delete_messages(chat_id=msg.from_user.id, message_ids=[i for i in range(msg.message_id-1, msg.message_id+1)])
    sqlite_db.add_list(owner_id=msg.from_user.id, name=msg.text)
    await msg.bot.edit_message_reply_markup(chat_id=msg.from_user.id, message_id=sqlite_db.get_message_id(id=msg.from_user.id), reply_markup=keyboards.lists_menu(msg.from_user.id)) 
@router.callback_query(States.lists)
async def lists(clbck: CallbackQuery, state: FSMContext):
    await state.set_state(state=States.list)
    await state.set_data({'list': clbck.data})
    await clbck.bot.edit_message_text(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, text=sqlite_db.get_list_name(int(clbck.data)))
    await clbck.bot.edit_message_reply_markup(message_id=sqlite_db.get_message_id(id=clbck.from_user.id), chat_id=clbck.from_user.id, reply_markup=keyboards.list_menu(int(clbck.data))) # TODO: list markup
@router.callback_query(F.data == Callbacks.delete_list.value)
async def delete_list(clbck: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    sqlite_db.delete_list(int(data['list']))
    await clbck.bot.edit_message_reply_markup(chat_id=clbck.from_user.id, message_id=sqlite_db.get_message_id(id=clbck.from_user.id), reply_markup=keyboards.lists_menu(clbck.from_user.id))

# * Tasks
@router.callback_query(F.data == Callbacks.add_new_task.value)
async def add_new_task(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer(text='Введите задачу')
    await state.set_state(States.set_task_name)

@router.message(States.set_task_name)
async def set_task_name(msg: Message, state: FSMContext):
    await state.set_data({'name':msg.text})
    await state.set_state(States.set_task_description)
    await msg.answer(text='Введите описание задачи')

@router.message(States.set_task_description)
async def set_task_description(msg: Message, state: FSMContext):
    data = await state.get_data()
    data['description'] = msg.text
    await state.set_data(data)

async def main():
    global dp, bot
    connect_db()

    bot = Bot(token=src.TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.set_my_description(BotMessages.bot_description.value)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types()) 

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())