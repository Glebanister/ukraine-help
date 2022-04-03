import logging
from typing import List, Callable, Optional, Dict, Tuple

import telegram
from telegram import ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToFailException
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.form.field.common_fields import field_select_language
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.localize.language import Language
from ua_help.telegram.util import make_buttons

OutputStream = Callable[[str], None]
TableRow = List[Tuple[str, str]]


class TextForm:
    def __init__(
            self,
            form_information: Localized,
            form_finish_information: Localized,
            localize: Callable[[Localized], str]
    ):
        self.form_information = form_information
        self.form_finish_information = form_finish_information
        self.localize = localize
        self.fields: List[FormField] = []
        self.filled_fields: List[Tuple[str, str]] = []

    def set_localize(self, localize: Callable[[Localized], str]):
        self.localize = localize
        for field in self.fields:
            field.set_localize(self.localize)

    def add_field(self, field: FormField):
        self.fields.append(field)
        field.set_localize(self.localize)

    def all_filled(self) -> bool:
        return len(self.filled_fields) == len(self.fields)

    def filled_fields(self) -> TableRow:
        return self.filled_fields

    def send_info_message(self, tg: TelegramContext):
        update, context = tg
        localized_info = self.localize(self.form_information)

        context.bot.send_message(
            text=localized_info,
            chat_id=update.effective_chat.id
        )

        if self.fields:
            self.fields[0].send_help(tg)

    def send_actual_field_info(self, tg: TelegramContext) -> None:
        update, context = tg
        assert not self.all_filled()
        self.fields[len(self.filled_fields)].send_help(tg)

    def put_user_input(self, user_input: str, tg: TelegramContext) -> Optional[TableRow]:
        update, context = tg

        if self.all_filled():
            raise ToFailException('TextForm', 'All fields are already read')
        cur_field = self.fields[len(self.filled_fields)]

        value_of_field = cur_field.try_read_value(user_input, tg)
        if value_of_field is not None:
            self.filled_fields.append((cur_field.key, value_of_field))
            if self.all_filled():
                context.bot.send_message(
                    text=self.localize(self.form_finish_information),
                    chat_id=update.effective_chat.id,
                    reply_markup=ReplyKeyboardMarkup(make_buttons(['/start', '/language', '/help']))
                )
                return self.filled_fields
            else:
                self.fields[len(self.filled_fields)].send_help(tg)
        else:
            cur_field.send_help(tg)
        return self.filled_fields if self.all_filled() else None
