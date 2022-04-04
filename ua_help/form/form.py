import logging
from typing import List, Callable, Optional, Dict, Tuple

import telegram
from telegram import ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToFailException
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.form.field.common_fields import field_select_language
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.localize.language import Language
from ua_help.telegram.util import make_reply_buttons

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
        self.active_field_index = 0

    def set_localize(self, localize: Callable[[Localized], str]):
        self.localize = localize
        for field in self.fields:
            field.set_localize(self.localize)

    def add_field(self, field: FormField):
        self.fields.append(field)
        field.set_localize(self.localize)

    def all_filled(self) -> bool:
        return self.active_field_index == len(self.fields)

    def filled_fields(self) -> TableRow:
        return self.filled_fields

    def send_help_for_current(self, tg: TelegramContext):
        update, context = tg
        next_field = self.active_field(tg)
        if next_field is None:
            context.bot.send_message(
                text=self.localize(self.form_finish_information),
                chat_id=update.effective_chat.id,
                reply_markup=make_reply_buttons(['/start', '/language', '/help'])
            )
            return self.filled_fields
        else:
            next_field.send_help(tg)

    def send_info_message(self, tg: TelegramContext):
        update, context = tg
        localized_info = self.localize(self.form_information)

        context.bot.send_message(
            text=f'*{localized_info}*',
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

        self.send_help_for_current(tg)

    def active_field(self, tg: TelegramContext) -> Optional[FormField]:
        while not self.all_filled() and self.fields[self.active_field_index].is_informational():
            self.fields[self.active_field_index].send_help(tg)
            self.active_field_index += 1
        return self.fields[self.active_field_index] if not self.all_filled() else None

    def send_actual_field_info(self, tg: TelegramContext) -> None:
        assert not self.all_filled()
        self.fields[self.active_field_index].send_help(tg)

    def put_user_input(self, user_input: str, tg: TelegramContext) -> Optional[TableRow]:
        update, context = tg

        field_to_put_info = self.active_field(tg)

        if self.all_filled():
            raise ToFailException('TextForm', 'All fields are already read')

        assert field_to_put_info is not None

        value_of_field = field_to_put_info.try_read_value(user_input, tg)
        if value_of_field is not None:
            self.filled_fields.append((field_to_put_info.key, value_of_field))
            self.active_field_index += 1
            self.send_help_for_current(tg)
        else:
            field_to_put_info.send_help(tg)
        return self.filled_fields if self.all_filled() else None
