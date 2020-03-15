from aiogram import __main__ as aiogram_core
from aiogram import types
from aiogram.dispatcher.filters import CommandHelp, CommandStart
from aiogram.utils.markdown import hbold, hlink, quote_html
from loguru import logger

from app.utils.keyboard import get_main_menu_markup
from app.misc import dp
from app.models.channel import Channel


@dp.message_handler(CommandStart())
async def cmd_start(message: types.Message):
    logger.info("User {user} start conversation with bot", user=message.from_user.id)
    await message.answer("Hello, {user}.\n".format(
            user=hbold(message.from_user.full_name)
        ), reply_markup=get_main_menu_markup()
    )
    # await Channel.create(chat_id='traveelto', name="Путешествуй с нами2")


    # await user.update(start_conversation=True).apply()

#
# @dp.message_handler(CommandHelp())
# async def cmd_help(message: types.Message):
#     logger.info("User {user} read help in {chat}", user=message.from_user.id, chat=message.chat.id)
#     text = [
#         hbold(_("Here you can read the list of my commands:")),
#         _("{command} - Start conversation with bot").format(command="/start"),
#         _("{command} - Get this message").format(command="/help"),
#         _("{command} - Chat or user settings").format(command="/settings"),
#         _("{command} - My version").format(command="/version"),
#         "",
#     ]
#
#     if types.ChatType.is_private(message):
#         text.extend(
#             [
#                 # hbold(_("Available only in PM with bot:")),
#                 # "",
#                 _("In chats this commands list can be other")
#             ]
#         )
#     else:
#         text.extend(
#             [
#                 hbold(_("Available only in groups:")),
#                 _("{command} - Report message to chat administrators").format(
#                     command="/report, !report, @admin"
#                 ),
#                 _("{command} - Set RO mode for user").format(command="!ro"),
#                 _("{command} - Ban user").format(command="!ban"),
#                 "",
#                 _("In private chats this commands list can be other"),
#             ]
#         )
#     await message.reply("\n".join(text))
#
#
# @dp.message_handler(commands=["version"])
# async def cmd_version(message: types.Message):
#     await message.reply(
#         _("My Engine:\n{aiogram}").format(aiogram=quote_html(str(aiogram_core.SysInfo())))
#     )


@dp.errors_handler()
async def errors_handler(update: types.Update, exception: Exception):
    try:
        raise exception
    except Exception as e:
        logger.exception("Cause exception {e} in update {update}", e=e, update=update)
    return True
