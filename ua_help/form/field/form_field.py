import abc
import logging
from typing import TypeVar, Generic, Optional, Callable, Tuple, List

import telegram
from telegram import Update
from telegram.ext import CallbackContext

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo, ToInformUserException
from ua_help.exception.field_invalid_fill_exception import FieldInvalidFillException
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import send_error

OutputStream = Callable[[str], None]
InputStream = Callable[[], str]
TelegramContext = Tuple[Update, CallbackContext]

T = TypeVar('T')


class FormField(Generic[T], abc.ABC):
    def __init__(
            self,
            key: str,
            label: Localized,
            default_value: Optional[T],
            localize: Optional[Callable[[Localized], str]]
    ):
        self.key = key
        self.label = label
        self.value: Optional[T] = None
        self.default_value = default_value
        self.localize = localize
        self.output: Optional[str] = None

    def loc_info(self, info: InfoMessage) -> str:
        if self.localize is None:
            raise Exception(f'localize for {self.key} is not set yet')
        return self.localize(info.value)

    def set_localize(self, localize: Callable[[Localized], str]):
        self.localize = localize

    def make_skip_text(self):
        return f'⏭️ {self.loc_info(InfoMessage.SKIP_TEXT_FIELD)} ⏭'

    def make_submit_text(self):
        return f'⏭️ {self.loc_info(InfoMessage.SUBMIT_MULTICHOICE)} ⏭'

    @staticmethod
    def make_question(text: str):
        return f'🟢 *{text}*'

    def make_information(self, text: Localized):
        return f'ℹ️ _{self.localize(text)}_'

    def make_is_required(self, is_required: bool) -> str:
        required_str = f'({self.loc_info(InfoMessage.NOT_REQUIRED)})'

        if is_required:
            required_str = f'- *{self.loc_info(InfoMessage.REQUIRED)}*'
        return required_str

    @abc.abstractmethod
    def send_help(self, tg: TelegramContext) -> None:
        pass

    @abc.abstractmethod
    def parse_input(self, s: str) -> Optional[T]:
        pass

    @abc.abstractmethod
    def repr_value(self, value: T) -> str:
        pass

    @abc.abstractmethod
    def validate_value(self, value: T) -> Optional[Localized]:
        pass

    @abc.abstractmethod
    def is_informational(self) -> bool:
        return False

    def has_no_default(self):
        return self.default_value is None

    def parse_and_set_value(self, string_repr: str) -> Optional[str]:
        if string_repr == '':
            return self.print_value()
        parsed_value = self.parse_input(string_repr)
        if parsed_value is None:
            return None
        if self.validate_value is not None:
            error = self.validate_value(parsed_value)
            if error is not None:
                raise FieldInvalidFillException(error)
        self.value = parsed_value
        return self.print_value()

    def print_value(self) -> str:
        if self.value is None:
            if self.default_value is None:
                raise ToInformUserExceptionWithInfo(InfoMessage.EMPTY_FIELD.value)
            else:
                return self.repr_value(self.default_value)
        return self.repr_value(self.value)

    def try_read_value(self, user_input: str, tg: TelegramContext) -> Optional[str]:
        try:
            self.output = self.parse_and_set_value(user_input)
            return self.output
        except ToInformUserException as e:
            send_error(f'{self.loc_info(InfoMessage.SOME_ERROR)}: {e.localized(self.localize)}', tg)
            return None
