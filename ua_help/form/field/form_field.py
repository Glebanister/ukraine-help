import abc
import logging
from typing import TypeVar, Generic, Optional, Callable

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo, ToInformUserException
from ua_help.exception.field_invalid_fill_exception import FieldInvalidFillException
from ua_help.localize.localize import Localized, InfoMessage

OutputStream = Callable[[str], None]
InputStream = Callable[[], str]

T = TypeVar('T')


class FormField(Generic[T], abc.ABC):
    def __init__(
            self,
            key: str,
            info: Localized,
            default_value: Optional[T],
            localize: Optional[Callable[[Localized], str]]
    ):
        self.key = key
        self.info = info
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

    @abc.abstractmethod
    def print_help(self) -> str:
        pass

    @abc.abstractmethod
    def parse_input(self, s: str) -> T:
        pass

    @abc.abstractmethod
    def repr_value(self, value: T) -> str:
        pass

    @abc.abstractmethod
    def validate_value(self, value: T) -> Optional[Localized]:
        pass

    def has_no_default(self):
        return self.default_value is None

    def parse_and_set_value(self, string_repr: str) -> str:
        if string_repr == '':
            return self.print_value()
        parsed_value = self.parse_input(string_repr)
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

    def print_info_to_stream(self, out_stream: OutputStream):
        out_stream(self.localize(self.info))

    def print_help_to_stream(self, out_stream: OutputStream):
        out_stream(self.print_help())

    def try_read_value(self, user_input: str, out_stream: OutputStream) -> Optional[str]:
        try:
            self.output = self.parse_and_set_value(user_input)
            return self.output
        except ToInformUserException as e:
            out_stream(f'{self.loc_info(InfoMessage.SOME_ERROR)}: {e.localized(self.localize)}')
            return None
