from contextlib import suppress
from functools import partial

from aiogram import types
from aiogram.utils.exceptions import MessageCantBeDeleted, MessageNotModified
from loguru import logger

from app.misc import bot, dp
from app.models.channel import Channel
from app.utils.keyboard import get_channel_list_markup
from app.utils.keyboard import cb_channel_settings


@dp.message_handler(text="⚙ Настройки")
async def channel_settings_handler(message: types.Message):
    logger.info("User {user} wants to configure", user=message.chat.id)
    all_channels = await Channel.query.gino.all()
    text, markup = get_channel_list_markup(all_channels)
    await message.answer(text=text, reply_markup=markup)


@dp.callback_query_handler(cb_channel_settings.filter(property="choose", value="edit"))
async def cq_channel_settings_edit(query: types.CallbackQuery, callback_data: dict):
    logger.info(
        "User {user} wants to change property in channel {channel}",
        user=query.from_user.id,
        channel=callback_data['id'],
    )

