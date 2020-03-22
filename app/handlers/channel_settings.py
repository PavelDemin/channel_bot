from contextlib import suppress
from functools import partial

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified
from loguru import logger
from aiogram.utils.markdown import hbold
from app.misc import bot, dp
from app.models.channel import Channel
from app.utils.keyboard import get_channel_list_markup
# from app.utils.keyboard import cb_channel_settings
from app.utils.keyboard import cb_channel_crud
from app.utils.keyboard import get_yes_no_inline_markup
from app.utils.keyboard import change_settings_channel_markup
from app.utils.keyboard import settings_channel_edit_markup
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from app.text import settings as st
import datetime


class ActionChannel(StatesGroup):
    chat_id = State()
    name = State()
    count_of_publications = State()
    start_time_publications = State()
    end_time_publications = State()
    is_enable = State()
    del_channel = State()


@dp.message_handler(text="⚙ Настройки", state="*")
async def channel_settings_handler(message: types.Message, state: FSMContext):
    logger.info("User {user} wants to configure", user=message.chat.id)
    await state.finish()
    all_channels = await Channel.query.gino.all()
    text, markup = get_channel_list_markup(all_channels)
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(cb_channel_crud.filter(property="edit"), state="*")
async def cq_channel_settings_edit(query: types.CallbackQuery, callback_data: dict):
    logger.info(
        "User {user} wants to change property in channel {id}",
        user=query.from_user.id,
        id=callback_data['value']
    )
    await types.CallbackQuery.answer(query)
    cs = await Channel.get(int(callback_data['value']))
    msg = st['chat_id'] + ": " + hbold(cs.chat_id) + "\n" + \
          st['name'] + ": " + hbold(cs.name) + "\n" + \
          st['publications_counter_total'] + ": " + hbold(cs.publications_counter_total) + "\n" + \
          st['publications_counter_day'] + ": " + hbold(cs.publications_counter_day) + "\n" + \
          st['last_publication_datetime'] + ": " + hbold(cs.last_publication_datetime) + "\n" + \
          st['count_of_publications'] + ": " + hbold(cs.count_of_publications) + "\n" + \
          st['start_time_publications'] + ": " + hbold(cs.start_time_publications) + "\n" + \
          st['end_time_publications'] + ": " + hbold(cs.end_time_publications) + "\n" + \
          st['is_enable'] + ": " + hbold(cs.is_enable) + "\n"
    await query.message.answer(text=msg, reply_markup=change_settings_channel_markup(cs.id))


@dp.callback_query_handler(cb_channel_crud.filter(property="edit_channel"))
async def cq_change_param_list(query: types.CallbackQuery, callback_data: dict):
    logger.info(
        "User {user} wants to change param list in channel {id}",
        user=query.from_user.id,
        id=callback_data['value']
    )
    await types.CallbackQuery.answer(query)
    await query.message.answer("Выберите параметр:", reply_markup=settings_channel_edit_markup())


@dp.callback_query_handler(cb_channel_crud.filter(property="edit_param"))
async def cq_change_param_channel(query: types.CallbackQuery, callback_data: dict):
    logger.info(
        "User {user} wants to change param {param} channel",
        user=query.from_user.id,
        param=callback_data['value']
    )
    await types.CallbackQuery.answer(query)


@dp.callback_query_handler(cb_channel_crud.filter(property="add", value="true"), state="*")
async def cq_add_channel(query: types.CallbackQuery):
    logger.info(
        "User {user} wants to add channel",
        user=query.from_user.id
    )
    await types.CallbackQuery.answer(query)
    await query.message.answer("Введите chat id канала:")
    await ActionChannel.chat_id.set()


@dp.message_handler(state=ActionChannel.chat_id)
async def state_input_chat_id(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input chat id:{chat_id}",
        user=message.from_user.id,
        chat_id=message.text
    )
    async with state.proxy() as data:
        data["chat_id"] = message.text.lower()
    await message.answer("Введите название канала:")
    await ActionChannel.name.set()


@dp.message_handler(state=ActionChannel.name)
async def state_input_name_channel(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input name:{name}",
        user=message.from_user.id,
        name=message.text
    )
    async with state.proxy() as data:
        data["name"] = message.text
    await message.answer("Введите необходимое количество публикаций в день:")
    await ActionChannel.count_of_publications.set()


@dp.message_handler(state=ActionChannel.count_of_publications)
async def state_input_count_of_publications_in_channel(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input count of publications in channel:{count_of_publications}",
        user=message.from_user.id,
        count_of_publications=message.text
    )
    async with state.proxy() as data:
        data["count_of_publications"] = message.text
    await message.answer("Введите время старта публикаций в формате " + hbold("HH:MM"))
    await ActionChannel.start_time_publications.set()


@dp.message_handler(state=ActionChannel.start_time_publications)
async def state_input_start_time_publications_in_channel(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input start time publications in channel:{start_time_publications}",
        user=message.from_user.id,
        start_time_publications=message.text
    )
    async with state.proxy() as data:
        data["start_time_publications"] = message.text
    await message.answer("Введите время конца публикаций в формате " + hbold("HH:MM"))
    await ActionChannel.end_time_publications.set()


@dp.message_handler(state=ActionChannel.end_time_publications)
async def state_input_end_time_publications_in_channel(message: types.Message, state: FSMContext):
    logger.info(
        "User {user} input end time publications in channel:{end_time_publications}",
        user=message.from_user.id,
        end_time_publications=message.text
    )
    async with state.proxy() as data:
        data["end_time_publications"] = message.text
    await message.answer("Активировать публикации в канал?", reply_markup=get_yes_no_inline_markup())
    await ActionChannel.is_enable.set()


@dp.callback_query_handler(cb_channel_crud.filter(property="bool"), state=ActionChannel.is_enable)
async def cb_input_is_enable_in_channel(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    logger.info(
        "User {user} input is enable in channel:{is_enable}",
        user=query.from_user.id,
        is_enable=callback_data["value"]
    )
    await types.CallbackQuery.answer(query)
    async with state.proxy() as data:
        start_time_publications = data["start_time_publications"].split(':')
        end_time_publications = data["end_time_publications"].split(':')
        await Channel.create(chat_id=data["chat_id"],
                             name=data["name"],
                             count_of_publications=int(data["count_of_publications"]),
                             start_time_publications=datetime.time(int(start_time_publications[0]),
                                                                   int(start_time_publications[1])),
                             end_time_publications=datetime.time(int(end_time_publications[0]),
                                                                 int(end_time_publications[1])),
                             is_enable=bool(int(callback_data["value"])))
    await query.message.answer("Канал успешно добавлен!")
    await state.finish()
    await channel_settings_handler(query.message, state)


@dp.callback_query_handler(cb_channel_crud.filter(property="del"), state="*")
async def cb_delete_channel_confirm(query: types.CallbackQuery, state: FSMContext, callback_data: dict):
    logger.info(
        "User {user} wont delete channel:{id}",
        user=query.from_user.id,
        id=callback_data["value"]
    )
    await types.CallbackQuery.answer(query)
    channel_item = await Channel.get(int(callback_data["value"]))
    async with state.proxy() as data:
        data["id"] = callback_data["value"]
    await ActionChannel.del_channel.set()
    await query.message.answer(f"Вы уверены, что хотите удалить канал: {hbold(channel_item.name)}",
                               reply_markup=get_yes_no_inline_markup())


@dp.callback_query_handler(cb_channel_crud.filter(property="bool"), state=ActionChannel.del_channel)
async def cb_delete_channel(query: types.CallbackQuery, state, callback_data: dict):
    logger.info(
        "User {user} wont delete channel:{bool}",
        user=query.from_user.id,
        bool=callback_data["value"]
    )
    await types.CallbackQuery.answer(query)
    if bool(int(callback_data["value"])):
        async with state.proxy() as data:
            await Channel.delete.where(Channel.id == int(data["id"])).gino.status()
            await query.answer("Канал успешно удален!")
    all_channels = await Channel.query.gino.all()
    text, markup = get_channel_list_markup(all_channels)
    await state.finish()
    await query.message.edit_text(text=text, reply_markup=markup)
