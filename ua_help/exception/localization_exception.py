from ua_help.exception.categorized_exception import ToFailException
from ua_help.localize.language import Language


class LocalizationException(ToFailException):
    def __init__(
            self,
            localization_error_message: str,
            text_to_translate: str,
            lang_from: Language,
            lang_to: Language
    ):
        formatted_message = f'Unable to localize text "{text_to_translate}" from {lang_from.value} to {lang_to.value}: ${localization_error_message}'
        super().__init__(type(self).__name__, formatted_message)


class TranslationException(LocalizationException):
    def __init__(
            self,
            reason: str,
            text_to_translate: str,
            lang_from: Language,
            lang_to: Language
    ):
        super().__init__(reason, text_to_translate, lang_from, lang_to)


class TranslationNotExistException(TranslationException):
    def __init__(
            self,
            text_to_translate: str,
            lang_from: Language,
            lang_to: Language):
        super().__init__("Dictionary does not contain translation", text_to_translate, lang_from, lang_to)
