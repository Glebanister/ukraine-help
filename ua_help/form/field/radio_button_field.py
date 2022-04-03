from typing import List, Callable, Optional, TypeVar, Tuple

import telegram
from telegram import ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.form.field.text_field import TextField
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
            is_required: bool,
            localize: Callable[[Localized], str] = None
    ):
        default_value = (Localized('', '', ''), '') if not is_required else None
        super().__init__(key, label, default_value, localize)
        self.choices = choices
        self.is_required = is_required

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        all_buttons = list(map(lambda choice: self.localize(choice[0]), self.choices))

        if not self.is_required:
            all_buttons.append(self.make_skip_text())

        context.bot.send_message(
            text=f'{TextField.make_question(self.localize(self.label))} {self.make_is_required(self.is_required)}',
            parse_mode=telegram.ParseMode.MARKDOWN,
            chat_id=update.effective_chat.id,
            reply_markup=ReplyKeyboardMarkup(
                keyboard=make_buttons(all_buttons),
                one_time_keyboard=True,
                resize_keyboard=True
            )
        )

    def parse_input(self, s: str) -> Tuple[Localized, R]:
        try:
            if s == self.make_skip_text():
                return self.default_value
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
