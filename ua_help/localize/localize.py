import dataclasses
import enum
import json
from pathlib import Path
from typing import List

from ua_help.localize.language import Language


@dataclasses.dataclass
class Localized:
    EN: str
    UA: str
    RU: str

    def translate_to(self, lang: Language):
        langs = {
            Language.EN: self.EN,
            Language.UA: self.UA,
            Language.RU: self.RU
        }
        return langs[lang]

    @classmethod
    def from_folder(cls, root: Path):
        def read_content(lang: Language) -> str:
            lang_path = (root / lang.name.lower()).with_suffix('.txt')
            with lang_path.open('r') as lang_file:
                return lang_file.read()

        return Localized(
            read_content(Language.EN),
            read_content(Language.UA),
            read_content(Language.RU),
        )

    @classmethod
    def choices_from_json(cls, path: Path):
        with path.open('r') as choices_json_file:
            json_content = choices_json_file.read()
            choices_as_json = json.loads(json_content)
            choices_list = []
            for choice in choices_as_json['choices']:
                choices_list.append((
                    Localized(choice['en'], choice['ua'], choice['ru']),
                    choice['id']
                ))
            return choices_list

    @classmethod
    def integers(cls, r: range, suffix) -> List:
        def make_loc_from_int(x: int):
            return (
                Localized(f'{x} {suffix.EN}', f'{x} {suffix.UA}', f'{x} {suffix.RU}'),
                str(x)
            )

        return list(map(make_loc_from_int, r))

    @classmethod
    def yes_no(cls) -> List:
        return [
            (Localized('Yes', 'Так', 'Да'), 'yes'),
            (Localized('No', 'Нi', 'Нет'), 'no'),
        ]


class InfoMessage(enum.Enum):
    SOME_ERROR = Localized(
        "Error",
        "Помилка",
        "Ошибка"
    )

    EMPTY_FIELD = Localized(
        "This field is required",
        "Це поле обов'язково для заповнення",
        "Это поле обязательно для заполнения",
    )

    FIELD_INVALID_FORMAT = Localized(
        "Invalid field format",
        "Неправильний формат",
        "Неправильный формат"
    )

    EMPTY_MULTICHOICE = Localized(
        "Choose at least one option",
        "Виберіть хоча б один варіант",
        "Выберите хотя бы один вариант"
    )

    LIST_WITH_COMMA = Localized(
        "Print the numbers of the selected options separated by commas",
        "Надрукуйте через кому номери вибраних варіантів",
        "Напечатайте через запятую номера выбранных вариантов"
    )

    CHOICE_NOT_IN_LIST = Localized(
        "Choice is not in list",
        "Варіант не у списку",
        "Вариант не в списке"
    )

    CHOOSE = Localized(
        "Choose",
        "Виберіть",
        "Выберите"
    )

    FROM = Localized(
        "from",
        "від",
        "от"
    )

    TO = Localized(
        "to",
        "до",
        "до"
    )

    CHOICE_PLURAL = Localized(
        "choices",
        "варіантів",
        "вариантов"
    )

    EACH_MUST_OCCUR_ONCE = Localized(
        "Each option must occur at most once",
        "Кожен варіант повинен зустрічатися не більше одного разу",
        "Каждый вариант должен встречаться не более одного раза"
    )

    CHOOSE_ONE_OPTION = Localized(
        "Print the number of the selected option",
        "Надрукуйте номер вибраного варіанта",
        "Напечатайте номер выбранного варианта"
    )

    INVALID_INPUT_FORMAT = Localized(
        "Invalid input format",
        "Неправильний формат введення",
        "Неправильный формат ввода"
    )

    INTERFACE_LANGUAGE = Localized(
        "Interface language",
        "Мова інтерфейсу",
        "Язык интерфейса"
    )

    LANG_RU = Localized(
        "Russian",
        "Російська",
        "Русский"
    )

    LANG_UA = Localized(
        "Ukrainian",
        "Українська",
        "Украинский"
    )

    LANG_US = Localized(
        "English",
        "Англійська",
        "Английский"
    )

    ALL_LANGUAGES = Localized(
        "All available languages",
        "Доступні мови",
        "Доступные языки"
    )

    INDEX_ERROR = Localized(
        "The typed index does not exist in the list",
        "Набраного індексу не існує у списку",
        "Набранного индекса не существует в списке"
    )

    EMAIL = Localized(
        "E-mail",
        "Електронна пошта для зв'язку",
        "Электронная почта для связи"
    )

    EMAIL_FORMAT = Localized(
        "example@something.com",
        "example@something.com",
        "example@something.com"
    )

    TELEGRAM = Localized(
        "Telegram handle",
        "Ваш логін у телеграм",
        "Ваш логин в телеграм"
    )

    TELEGRAM_FORMAT = Localized(
        "@telegram_username_example",
        "@telegram_username_example",
        "@telegram_username_example"
    )

    INPUT_FORMAT = Localized(
        "Input format",
        "Формат введення",
        "Формат ввода"
    )

    PLEASE_INPUT = Localized(
        "Input",
        "Введіть",
        "Введите"
    )

    REQUIRED = Localized(
        "Required",
        "Обов'язково",
        "Обязательно"
    )

    NOT_REQUIRED = Localized(
        "Not required",
        "Не обов'язково",
        "Не обязательно"
    )
