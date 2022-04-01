import re
from typing import Optional, Callable

from ua_help.form.field.form_field import FormField
from ua_help.localize.localize import Localized, InfoMessage


class TextField(FormField[str]):
    def __init__(
            self,
            key: str,
            info: Localized,
            pattern: re.Pattern,
            pattern_explanation: Localized,
            is_required: bool,
            localize: Optional[Callable[[Localized], str]] = None
    ):
        super().__init__(key, info, None, localize)
        self.pattern = pattern
        self.pattern_explanation = pattern_explanation
        self.is_required = is_required

    def print_help(self) -> str:
        required_str = self.loc_info(InfoMessage.NOT_REQUIRED) if not self.is_required else self.loc_info(
            InfoMessage.REQUIRED)
        return f'''
{self.loc_info(InfoMessage.PLEASE_INPUT)} {self.localize(self.info)} ({required_str})
{self.loc_info(InfoMessage.INPUT_FORMAT)}: {self.localize(self.pattern_explanation)}
'''

    def parse_input(self, s: str) -> str:
        return s

    def repr_value(self, value: str) -> str:
        return value

    def validate_value(self, value: str) -> Optional[Localized]:
        if re.match(self.pattern, value) is None:
            return InfoMessage.INVALID_INPUT_FORMAT.value
        return None
