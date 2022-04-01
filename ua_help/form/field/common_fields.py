import re
from typing import Callable

from ua_help.form.field.form_field import FormField
from ua_help.form.field.radio_button_field import RadioButtonField
from ua_help.form.field.text_field import TextField
from ua_help.localize.localize import Localized
from ua_help.localize.language import Language


def field_select_language() -> FormField:
    def localize_to_all(info: Localized) -> str:
        return '/'.join(map(lambda lang: info.translate_to(lang), list(Language)))

    return RadioButtonField(
        'language',
        Localized("Interface language", "Виберіть мову інтерфейсу", "Выберите язык интерфейса"),
        [
            (Localized("English", "Англійська", "Английский"), Language.EN),
            (Localized("Ukrainian", "Українська", "Украинский"), Language.UA),
            (Localized("Russian", "Російська", "Русский"), Language.RU),
        ],
        localize_to_all,
    )


def field_email(is_required: bool) -> FormField:
    return TextField(
        'email',
        Localized("E-mail", "Електронна пошта", "Электронная почта"),
        re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        Localized("some@thing.com", "some@thing.com", "some@thing.com"),
        is_required,
    )


def field_telegram(is_required: bool) -> FormField:
    return TextField(
        'telegram',
        Localized("Telegram", "Логин в телеграм (начинается с @)", "Логін у телеграм (починається з @)"),
        re.compile(r'.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*'),
        Localized("@some_user", "@some_user", "@some_user"),
        is_required,
    )
