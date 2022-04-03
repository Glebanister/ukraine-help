import dataclasses
from typing import Callable, List, Optional, Iterable, TypeVar, Tuple

import telegram
from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

from ua_help.exception.categorized_exception import ToInformUserWithLocalizedMessage
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.localize.localize import Localized, InfoMessage
from ua_help.telegram.util import make_buttons

R = TypeVar('R')

MultipleChoice = List[Tuple[Localized, R]]

OPTION_NOT_CHOSEN = '➖'
OPTION_CHOSEN = '✅'


@dataclasses.dataclass
class Option:
    localized: Localized
    value: R
    chosen: bool


class MultipleVariantsField(FormField[MultipleChoice]):
    def is_informational(self) -> bool:
        return False

    def __init__(
            self,
            key: str,
            label: Localized,
            choices: List[Tuple[Localized, R]],
            default_choice: Optional[MultipleChoice],
            bound_min: Optional[int],
            bound_max: Optional[int],
            localize: Optional[Callable[[Localized], str]] = None
    ):
        super().__init__(key, label, default_choice, localize)
        self.choices = list(map(lambda choice: Option(choice[0], choice[1], False), choices))
        self.bound_min = bound_min
        self.bound_max = bound_max

    def localized_choices(self) -> Iterable[str]:

        def format_choice(choice: Option) -> str:
            localized_choice = self.localize(choice.localized)
            if_chosen = OPTION_CHOSEN if choice.chosen else OPTION_NOT_CHOSEN
            return f'{if_chosen} {localized_choice}'

        return list(map(format_choice, self.choices)) + [f'{self.localize(InfoMessage.SUBMIT_MULTICHOICE.value)}']

    def chosen_count(self):
        return sum(map(lambda choice: int(choice.chosen), self.choices))

    def __must_choose_some_but_not(self) -> bool:
        return self.bound_min is not None and self.bound_min == 1 and self.chosen_count() == 0

    def __matches_min_bound(self) -> bool:
        return self.bound_min is None or self.bound_min <= self.chosen_count()

    def __matches_max_bound(self) -> bool:
        return self.bound_max is None or self.chosen_count() <= self.bound_max

    def __get_min_bound_underflow(self) -> int:
        if self.bound_min is None:
            return 0
        underflow = self.bound_min - self.chosen_count()
        return max(underflow, 0)

    def __get_max_bound_overflow(self) -> int:
        if self.bound_max is None:
            return 0
        overflow = self.chosen_count() - self.bound_max
        return max(overflow, 0)

    def __make_overflow_message(self) -> str:
        return f'{self.loc_info(InfoMessage.CAN_CHOOSE_NO_MORE_THAN)} {self.bound_max} {self.loc_info(InfoMessage.CHOICE_PLURAL)}'

    def __make_underflow_message(self):
        return f'{self.loc_info(InfoMessage.MUST_CHOOSE_AT_LEAST)} {self.bound_min} {self.loc_info(InfoMessage.CHOICE_PLURAL)}'

    def send_help(self, tg: TelegramContext) -> None:
        update, context = tg

        bounds_str = ''

        if self.__must_choose_some_but_not():
            bounds_str += self.loc_info(InfoMessage.PLEASE_CHOOSE_AT_LEAST_ONE)
        else:
            overflow = self.__get_max_bound_overflow()
            underflow = self.__get_min_bound_underflow()

            if overflow > 0:
                bounds_str += self.__make_overflow_message()
            elif underflow > 0:
                bounds_str += self.__make_underflow_message()

        how_to_submit = ''
        if not bounds_str:
            how_to_submit += f"{self.loc_info(InfoMessage.IF_YOU_FINISHED_SUBMIT)} '{self.loc_info(InfoMessage.SUBMIT_MULTICHOICE)}'"

        context.bot.send_message(
            text=f'*{self.localize(self.label)}*\n{bounds_str}{how_to_submit}',
            chat_id=update.effective_chat.id,
            parse_mode=telegram.ParseMode.MARKDOWN,
            reply_markup=ReplyKeyboardMarkup(make_buttons(self.localized_choices()))
        )

    def __add_option(self, index: int) -> None:
        assert index < len(self.choices)
        assert not self.choices[index].chosen
        self.choices[index].chosen = True

    def __remove_option(self, index: int) -> None:
        assert index < len(self.choices)
        assert self.choices[index].chosen
        self.choices[index].chosen = False

    def __submit_choice(self) -> MultipleChoice:
        if not self.__matches_max_bound():
            raise ToInformUserWithLocalizedMessage(self.__make_overflow_message())
        if self.__must_choose_some_but_not():
            raise ToInformUserWithLocalizedMessage(
                f'{self.loc_info(InfoMessage.EMPTY_MULTICHOICE)}'
            )
        if not self.__matches_min_bound():
            raise ToInformUserWithLocalizedMessage(self.__make_underflow_message())

        return list(map(
            lambda option: (option.localized, option.value),
            filter(lambda option: option.chosen, self.choices)
        ))

    def parse_input(self, user_input: str) -> Optional[MultipleChoice]:
        try:
            user_input_index = list(self.localized_choices()).index(user_input)
            if user_input_index == len(self.choices):
                return self.__submit_choice()
            elif self.choices[user_input_index].chosen:
                self.__remove_option(user_input_index)
            else:
                self.__add_option(user_input_index)
            return None
        except ValueError:
            raise ToInformUserWithLocalizedMessage(
                f'{self.loc_info(InfoMessage.CHOICE_NOT_IN_LIST)}: {user_input}')

    def repr_value(self, value: MultipleChoice) -> str:
        return ', '.join(map(lambda choice: f'{choice[1]}', value))

    def validate_value(self, value: MultipleChoice) -> Optional[Localized]:
        if self.bound_min is None and self.bound_max is None:
            return None
        if self.bound_min == 1 and value == []:
            return InfoMessage.EMPTY_MULTICHOICE.value
        return None
