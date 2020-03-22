from typing import Tuple

from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.callback_data import CallbackData
from aiogram.utils.markdown import hbold
from app.text import text as t
from app.text import settings as st
from app.models.channel import Channel

# cb_channel_settings = CallbackData("channel", "id", "property", "value")
cb_channel_crud = CallbackData("crud", "property", "value")

FLAG_STATUS = ["❌", "✅"]


def get_main_menu_markup():
    return ReplyKeyboardMarkup(resize_keyboard=True, selective=True, keyboard=[
        [
            KeyboardButton(text=t['settings'])
        ]
    ])


def get_channel_list_markup(channels: list) -> Tuple[str, InlineKeyboardMarkup]:
    inline_keyboard = [
        [
            InlineKeyboardButton(
                text=channel.name,
                callback_data=cb_channel_crud.new(
                    property="edit",
                    value=channel.id
                )
            ),
            InlineKeyboardButton(
                text="❌",
                callback_data=cb_channel_crud.new(
                    property="del",
                    value=channel.id
                )
            )
        ] for channel in channels]
    inline_keyboard.append([
        InlineKeyboardButton(
            text=t['add_channel'],
            callback_data=cb_channel_crud.new(
                property="add",
                value="true"
            )
        )
    ])
    return (
        "Список каналов:",
        InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )
    )


def get_yes_no_inline_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Да",
                    callback_data=cb_channel_crud.new(
                        property="bool",
                        value="1"
                    )
                ),
                InlineKeyboardButton(
                    text="Нет",
                    callback_data=cb_channel_crud.new(
                        property="bool",
                        value="0"
                    )
                )
            ]
        ]
    )


def change_settings_channel_markup(channel) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Изменить настройки",
                    callback_data=cb_channel_crud.new(
                        property="edit_channel",
                        value=channel
                    )
                )
            ]
        ]
    )


def settings_channel_list() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Изменить настройки",
                    callback_data=cb_channel_crud.new(
                        property="edit_channel",
                        value="channel"
                    )
                )
            ]
        ]
    )


def settings_channel_edit_markup() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=st[param],
                    callback_data=cb_channel_crud.new(
                        property="edit_param",
                        value=param
                    )
                )
            ] for param in st]

    )

# def get_channel_settings_markup(
#     telegram_chat: types.Chat, chat: Chat
# ) -> Tuple[str, InlineKeyboardMarkup]:
#     return (
#         _("Settings for chat {chat_title}").format(chat_title=hbold(telegram_chat.title)),
#         InlineKeyboardMarkup(
#             inline_keyboard=[
#                 [
#                     InlineKeyboardButton(
#                         text=_("{status} Join filter").format(
#                             status=FLAG_STATUS[chat.join_filter]
#                         ),
#                         callback_data=cb_chat_settings.new(
#                             id=chat.id, property="join", value="switch"
#                         ),
#                     )
#                 ],
#                 [
#                     InlineKeyboardButton(
#                         text=_("{flag} Language").format(
#                             flag=i18n.AVAILABLE_LANGUAGES[chat.language].flag
#                         ),
#                         callback_data=cb_chat_settings.new(
#                             id=chat.id, property="language", value="change"
#                         ),
#                     )
#                 ],
#                 [
#                     InlineKeyboardButton(
#                         text=_("Done"),
#                         callback_data=cb_chat_settings.new(
#                             id=chat.id, property="done", value="true"
#                         ),
#                     )
#                 ],
#             ]
#         ),
#     )
