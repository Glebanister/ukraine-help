from typing import List, TypeVar, Tuple, Callable, Iterable

import telegram
from telegram import InlineKeyboardButton, Update, KeyboardButton
from telegram.ext import CallbackContext

from ua_help.localize.localize import Localized

V = TypeVar('V')

TelegramContext = Tuple[Update, CallbackContext]


def make_buttons(args: Iterable[str]) -> List[List[KeyboardButton]]:
    return list(map(lambda txt: [KeyboardButton(txt)], args))


def send_error(message: str, tg: TelegramContext) -> None:
    update, context = tg
    context.bot.send_message(
        text=f'⚠️ _{message}️_',
        chat_id=update.effective_chat.id,
        parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def send_plain_text(message: str, tg: TelegramContext) -> None:
    update, context = tg
    context.bot.send_message(
        text=message,
        chat_id=update.effective_chat.id
    )
