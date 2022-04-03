import re
from typing import Optional, Callable

import telegram
from telegram import ReplyKeyboardRemove, ReplyKeyboardMarkup

from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_buttons


class TextField(FormField[str]):
    def is_informational(self) -> bool:
        return False

    def __init__(
            self,
            key: str,
            label: Localized,
            pattern: re.Pattern,
            pattern_explanation: Localized,
            is_required: bool,
            localize: Optional[Callable[[Localized], str]] = None
    ):
        super().__init__(key, label, None, localize)
        self.pattern = pattern
        self.pattern_explanation = pattern_explanation
        self.is_required = is_required

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        required_str = f'({self.loc_info(InfoMessage.NOT_REQUIRED)})'

        if self.is_required:
            required_str = f'- *{self.loc_info(InfoMessage.REQUIRED)}*'

        help_markdown = f'''
{self.loc_info(InfoMessage.PLEASE_INPUT)} {self.localize(self.label)} {required_str}
{self.loc_info(InfoMessage.INPUT_FORMAT)}: _{self.localize(self.pattern_explanation)}_
        '''

        def make_skip_button():
            return make_buttons([self.loc_info(InfoMessage.SKIP_TEXT_FIELD)])

        context.bot.send_message(
            text=help_markdown,
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove() if self.is_required else ReplyKeyboardMarkup(make_skip_button())
        )

    def parse_input(self, s: str) -> str:
        if s == self.loc_info(InfoMessage.SKIP_TEXT_FIELD):
            return ''
        return s

    def repr_value(self, value: str) -> str:
        return value

    def validate_value(self, value: str) -> Optional[Localized]:
        if re.match(self.pattern, value) is None:
            return InfoMessage.INVALID_INPUT_FORMAT.value
        return None
