from typing import List, Callable, Optional, TypeVar, Tuple

import telegram
from telegram import ReplyKeyboardMarkup, Message

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.form.field.text_field import TextField
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_with_message_buttons

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
            allow_choose_other: bool,
            localize: Callable[[Localized], str] = None
    ):
        default_value = (Localized('', '', ''), '') if not is_required else None
        super().__init__(key, label, default_value, localize)
        self.choices = choices
        self.is_required = is_required
        self.allow_choose_other = allow_choose_other

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        all_buttons = list(map(lambda choice: (self.localize(choice[0]), choice[1]), self.choices))

        question_message = f'{TextField.make_question(self.localize(self.label))} {self.make_is_required(self.is_required)}'

        if self.allow_choose_other:
            question_message += f'\n\nℹ️ {self.loc_info(InfoMessage.INPUT_OTHER_WITH_KEYBOARD)}'

        if not self.is_required:
            all_buttons.append(self.make_skip_text())

        kwargs = {
            'text': question_message,
            'chat_id': update.effective_chat.id,
            'parse_mode': telegram.ParseMode.MARKDOWN,
            'reply_markup': make_with_message_buttons(all_buttons)
        }

        if self.message is not None:
            kwargs['message_id'] = self.message.message_id
            context.bot.edit_message_text(**kwargs)
        else:
            self.message = context.bot.send_message(**kwargs)

    def parse_input(self, s: str) -> Optional[Tuple[Localized, R]]:
        try:
            if s in self.make_skip_text():
                return self.default_value
            matches = list(filter(lambda choice: choice[1] == s, self.choices))
            if not matches:
                if self.allow_choose_other:
                    return InfoMessage.OTHER_OPTION.value, s
                raise ValueError()
            return matches[0]
        except ValueError:
            raise ToInformUserExceptionWithInfo(InfoMessage.INVALID_INPUT_FORMAT.value)

    def repr_value(self, value: Tuple[Localized, R]) -> str:
        return str(value[1])

    def validate_value(self, value: Tuple[Localized, R]) -> Optional[Localized]:
        pass
