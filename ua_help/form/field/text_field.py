import re
from typing import Optional, Callable

import telegram
from telegram import ReplyKeyboardRemove

from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_with_message_buttons


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

        question = FormField.make_question(f'{self.loc_info(InfoMessage.PLEASE_INPUT)} {self.localize(self.label)}')

        help_markdown = f'''{question} {self.make_is_required(self.is_required)}
{self.loc_info(InfoMessage.INPUT_FORMAT)}: _{self.localize(self.pattern_explanation)}_
'''

        self.message = context.bot.send_message(
            text=help_markdown,
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardRemove() if self.is_required else make_with_message_buttons(
                [self.make_skip_text()])
        )

    def parse_input(self, s: str) -> str:
        if s in self.make_skip_text():
            return ''
        return s

    def repr_value(self, value: str) -> str:
        return value

    def validate_value(self, value: str) -> Optional[Localized]:
        if re.match(self.pattern, value) is None:
            return InfoMessage.INVALID_INPUT_FORMAT.value
        return None
