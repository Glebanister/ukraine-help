from typing import Callable, List, Optional, Iterable, TypeVar, Tuple

from ua_help.exception.categorized_exception import ToInformUserWithLocalizedMessage
from ua_help.form.field.form_field import FormField
from ua_help.localize.localize import Localized, InfoMessage

R = TypeVar('R')

MultipleChoice = List[Tuple[Localized, R]]


class MultipleVariantsField(FormField[MultipleChoice]):
    def __init__(
            self,
            key: str,
            label: Localized,
            choices: MultipleChoice,
            default_choice: Optional[MultipleChoice],
            bound_min: Optional[int],
            bound_max: Optional[int],
            localize: Optional[Callable[[Localized], str]] = None
    ):
        super().__init__(key, label, default_choice, localize)
        self.choices = choices
        self.bound_min = bound_min
        self.bound_max = bound_max

    def localized_choices(self) -> Iterable[str]:
        return map(self.localize, map(lambda x: x[0], self.choices))

    def print_help(self) -> str:
        choices = '\n'.join(map(lambda item: f'  {item[0] + 1}) {item[1]}', enumerate(self.localized_choices())))
        bounds_min_str = f'{self.loc_info(InfoMessage.FROM)} {self.bound_min} ' if self.bound_min is not None else ''
        bounds_max_str = f'{self.loc_info(InfoMessage.TO)} {self.bound_max} ' if self.bound_max is not None else ''
        bounds_str = f'{self.loc_info(InfoMessage.CHOOSE)} {bounds_min_str}{bounds_max_str}{self.loc_info(InfoMessage.CHOICE_PLURAL)}'

        return f'''{choices}
{self.loc_info(InfoMessage.LIST_WITH_COMMA)}
{bounds_str}
'''

    def parse_input(self, s: str) -> MultipleChoice:
        user_choices: List[str] = list(map(lambda x: x.strip(), s.split(',')))
        chosen: MultipleChoice = []
        for user_choice in user_choices:
            try:
                s_as_index = int(user_choice) - 1
                s_as_choice = self.choices[s_as_index]
                if s_as_choice in chosen:
                    raise ToInformUserWithLocalizedMessage(
                        f'{self.loc_info(InfoMessage.EACH_MUST_OCCUR_ONCE)} ({user_choice})')
                chosen.append(s_as_choice)
            except ValueError:
                raise ToInformUserWithLocalizedMessage(
                    f'{self.loc_info(InfoMessage.INVALID_INPUT_FORMAT)}: {user_choice}')
            except IndexError:
                raise ToInformUserWithLocalizedMessage(f'{self.loc_info(InfoMessage.INDEX_ERROR)}: {user_choice}')
        return chosen

    def repr_value(self, value: MultipleChoice) -> str:
        return ', '.join(map(lambda choice: f'{choice[1]}', value))

    def validate_value(self, value: MultipleChoice) -> Optional[Localized]:
        if self.bound_min is None and self.bound_max is None:
            return None
        if self.bound_min == 1 and value == []:
            return InfoMessage.EMPTY_MULTICHOICE.value
        return None
