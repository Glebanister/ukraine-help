import logging
from typing import List, Callable, Optional, Dict, Tuple

from ua_help.exception.categorized_exception import ToFailException
from ua_help.form.field.form_field import FormField
from ua_help.form.field.common_fields import field_select_language
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.localize.language import Language

OutputStream = Callable[[str], None]
TableRow = List[Tuple[str, str]]


class TextForm:
    def __init__(
            self,
            info: Localized,
            localize: Callable[[Localized], str]
    ):
        self.info = info
        self.localize = localize
        self.fields: List[FormField] = []
        self.filled_fields: List[Tuple[str, str]] = []

    def add_field(self, field: FormField):
        self.fields.append(field)
        field.set_localize(self.localize)

    def all_filled(self) -> bool:
        return len(self.filled_fields) == len(self.fields)

    def filled_fields(self) -> TableRow:
        return self.filled_fields

    def print_info_to_stream(self, out_stream: OutputStream):
        localized_info = self.localize(self.info)
        out_stream(self.localize(self.info))
        if self.fields:
            self.fields[0].print_info_to_stream(out_stream)
            self.fields[0].print_help_to_stream(out_stream)

    def put_user_input(self, user_input: str, out_stream: OutputStream) -> Optional[TableRow]:
        if self.all_filled():
            raise ToFailException('TextForm', 'All fields are already read')
        cur_field = self.fields[len(self.filled_fields)]
        value_of_field = cur_field.try_read_value(user_input, out_stream)
        if value_of_field is not None:
            self.filled_fields.append((cur_field.key, value_of_field))
            if self.all_filled():
                out_stream(self.localize(InfoMessage.FINISH_STUDENT_INPUT.value))
                return self.filled_fields
            else:
                self.fields[len(self.filled_fields)].print_info_to_stream(out_stream)
                self.fields[len(self.filled_fields)].print_help_to_stream(out_stream)
        else:
            cur_field.print_help_to_stream(out_stream)
        return self.filled_fields if self.all_filled() else None
