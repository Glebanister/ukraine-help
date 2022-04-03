from typing import List, Callable, Optional, TypeVar, Tuple

import telegram
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_buttons

R = TypeVar('R')


class RadioButtonField(FormField[Tuple[Localized, R]]):
    def is_informational(self) -> bool:
        return False

    def __init__(
            self,
            key: str,
            label: Localized,
            choices: List[Tuple[Localized, R]],
            localize: Callable[[Localized], str] = None
    ):
        super().__init__(key, label, None, localize)
        self.choices = choices

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        context.bot.send_message(
            text=f'*{self.localize(self.label)}*',
            parse_mode=telegram.ParseMode.MARKDOWN,
            chat_id=update.effective_chat.id,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=make_buttons(map(lambda choice: self.localize(choice[0]), self.choices)),
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )

    def parse_input(self, s: str) -> Tuple[Localized, R]:
        try:
            matches = list(filter(lambda choice: self.localize(choice[0]) == s, self.choices))
            if not matches:
                raise ValueError()
            return matches[0]
        except ValueError:
            raise ToInformUserExceptionWithInfo(InfoMessage.INVALID_INPUT_FORMAT.value)

    def repr_value(self, value: Tuple[Localized, R]) -> str:
        return str(value[1])

    def validate_value(self, value: Tuple[Localized, R]) -> Optional[Localized]:
        pass
