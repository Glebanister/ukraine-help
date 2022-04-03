import re
from typing import Optional, Callable

import telegram
from telegram import InlineKeyboardMarkup, ReplyKeyboardRemove, ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToFailException
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_buttons


class InfoField(FormField[str]):
    def __init__(
            self,
            label: Localized,
            information: Localized,
            localize: Optional[Callable[[Localized], str]] = None
    ):
        super().__init__('', label, None, localize)
        self.information = information

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        context.bot.send_message(
            text=f'*{self.localize(self.label)}*\n\n{self.localize(self.information)}',
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.MARKDOWN
        )

    def is_informational(self) -> bool:
        return True

    def parse_input(self, s: str) -> str:
        raise ToFailException('InfoField', 'can not parse anything')

    def repr_value(self, value: str) -> str:
        raise ToFailException('InfoField', 'can not repr anything')

    def validate_value(self, value: str) -> Optional[Localized]:
        raise ToFailException('InfoField', 'can not validate anything')
