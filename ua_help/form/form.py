from typing import List, Callable, Optional, Dict

from ua_help.form.field.form_field import FormField
from ua_help.form.field.common_fields import field_select_language
from ua_help.localize.localize import Localized
from ua_help.localize.language import Language


class TextForm:
    def __init__(
            self,
            info: Localized,
            input_stream: Callable[[], str],
            output_stream: Callable[[str], None]
    ):
        self.info = info
        self.fields: List[FormField] = []
        self.input_stream = input_stream
        self.output_stream = output_stream
        self.localize: Optional[Callable[[Localized], str]] = None

    def add_field(self, field: FormField):
        self.fields.append(field)

    def read_fields(self) -> Dict[str, str]:
        form_dict: Dict[str, str] = {}
        if self.localize is None:
            language_field = field_select_language()
            language = language_field.read_value_retrying(self.input_stream, self.output_stream)
            self.localize = lambda localized: localized.translate_to(Language.from_str(language))
        self.output_stream(self.localize(self.info))
        for field in self.fields:
            field.set_localize(self.localize)
            form_dict[field.key] = field.read_value_retrying(self.input_stream, self.output_stream)
        return form_dict
