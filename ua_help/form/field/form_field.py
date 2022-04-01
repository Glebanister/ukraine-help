import abc
from typing import TypeVar, Generic, Optional, Callable

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo, ToInformUserException
from ua_help.exception.field_invalid_fill_exception import FieldInvalidFillException
from ua_help.localize.localize import Localized, InfoMessage

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

    def read_value_retrying(self, input_stream: Callable[[], str], out_stream: Callable[[str], None]) -> str:
        out_stream(self.localize(self.info))
        output = None
        while output is None:
            out_stream(self.print_help())
            another_input = input_stream()
            try:
                output = self.parse_and_set_value(another_input)
            except ToInformUserException as e:
                out_stream(f'{self.loc_info(InfoMessage.SOME_ERROR)}: {e.localized(self.localize)}')
        return output
