from typing import List, Callable, Optional, TypeVar, Tuple

from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo
from ua_help.form.field.form_field import FormField
from ua_help.localize.localize import Localized, InfoMessage

R = TypeVar('R')


class RadioButtonField(FormField[Tuple[Localized, R]]):
    def __init__(
            self,
            key: str,
            label: Localized,
            choices: List[Tuple[Localized, R]],
            localize: Callable[[Localized], str] = None
    ):
        super().__init__(key, label, None, localize)
        self.choices = choices

    def print_help(self) -> str:
        choices = '\n'.join(
            map(
                lambda item: f'  {item[0] + 1}) {item[1]}',
                enumerate(map(self.localize, map(lambda x: x[0], self.choices))))
        )
        return f'''{choices}
{self.loc_info(InfoMessage.CHOOSE_ONE_OPTION)}
'''

    def parse_input(self, s: str) -> Tuple[Localized, R]:
        try:
            index = int(s.strip())
            return self.choices[index - 1]
        except ValueError:
            raise ToInformUserExceptionWithInfo(InfoMessage.INVALID_INPUT_FORMAT.value)
        except IndexError:
            raise ToInformUserExceptionWithInfo(InfoMessage.INDEX_ERROR.value)

    def repr_value(self, value: Tuple[Localized, R]) -> str:
        return str(value[1])

    def validate_value(self, value: Tuple[Localized, R]) -> Optional[Localized]:
        pass
