import math
from typing import List, TypeVar, Tuple, Callable, Iterable, Optional

import telegram
from telegram import InlineKeyboardButton, Update, KeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from telegram.ext import CallbackContext

V = TypeVar('V')

TelegramContext = Tuple[Update, CallbackContext]

ArgT = TypeVar('ArgT')

Arranger = Callable[[Iterable[ArgT]], List[List[ArgT]]]


def arrange_buttons_with_limit(extract_len: Callable[[ArgT], int]) -> Callable[[Iterable[ArgT]], List[List[ArgT]]]:
    def arranger(args: Iterable[ArgT]):
        max_chars_per_line = 20
        args_list = list(args)
        n_args = len(args_list)
        current_line_chars = 0
        lines: List[List[str]] = []
        current_line: List[str] = []
        for arg_i in range(n_args):
            if current_line_chars + extract_len(args_list[arg_i]) > max_chars_per_line:
                lines.append(current_line)
                current_line = []
                current_line_chars = 0
            current_line.append(args_list[arg_i])
            current_line_chars += extract_len(args_list[arg_i])
        if current_line:
            lines.append(current_line)
        return lines

    return arranger


def arrange_buttons_vertically(args: Iterable[str]) -> List[List[str]]:
    return list(map(lambda arg: [arg], args))


def arrange_buttons_horizontally(args: Iterable[str]) -> List[List[str]]:
    return [list(args)]


ButtonT = TypeVar('ButtonT')


def make_buttons_with_arranger(
        args: Iterable[ArgT],
        arranger: Arranger,
        to_button: Callable[[ArgT], ButtonT]
) -> List[List[ButtonT]]:
    arranged = map(lambda buttons_row: list(map(to_button, buttons_row)), arranger(args))
    return list(arranged)


def make_with_message_buttons(
        args: Iterable[Tuple[str, str]],
        *,
        arranger: Arranger = arrange_buttons_with_limit(lambda xy: len(xy[0])),
        **kwargs,
) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        make_buttons_with_arranger(
            args,
            arranger,
            lambda name_callback: InlineKeyboardButton(name_callback[0], callback_data=name_callback[1])
        ),
        **kwargs
    )


def make_reply_buttons(
        args: Iterable[str],
        *,
        arranger: Arranger = arrange_buttons_vertically,
        **kwargs
) -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        make_buttons_with_arranger(
            args,
            arranger,
            lambda name: KeyboardButton(name)
        ),
        **kwargs
    )


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
