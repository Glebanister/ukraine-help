import re

from ua_help.form.field.form_field import FormField
from ua_help.form.field.radio_button_field import RadioButtonField
from ua_help.localize.localize import Localized
from ua_help.localize.language import Language


def field_select_language() -> FormField:
    def localize_to_non_empty(info: Localized) -> str:
        translated_to_all = map(lambda lang: info.translate_to(lang), list(Language))
        return '/'.join(filter(lambda tr: tr != '', translated_to_all))

    return RadioButtonField(
        key='language',
        label=Localized("Interface language", "Виберіть мову інтерфейсу", "Выберите язык интерфейса"),
        choices=[
            (Localized('🇬🇧 English', '', ''), 'en'),
            (Localized('🇺🇦 Українська', '', ''), 'ua'),
            (Localized('🇷🇺 Русский', '', ''), 'ru'),
        ],
        is_required=True,
        allow_choose_other=False,
        localize=localize_to_non_empty,
    )
