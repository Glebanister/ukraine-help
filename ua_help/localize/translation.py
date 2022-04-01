import abc

from typing import Dict, NoReturn

from ua_help.localize.language import Language
from ua_help.exception.localization_exception import (
    TranslationException,
    TranslationNotExistException
)


class Translator(abc.ABC):
    def __init__(
            self,
            lang_from: Language,
            lang_to: Language
    ):
        self.lang_from = lang_from
        self.lang_to = lang_to

    @abc.abstractmethod
    def translate(self, text: str) -> str:
        pass

    def raise_translation_exception(self, message: str, text: str) -> NoReturn:
        raise TranslationException(message, text, self.lang_from, self.lang_to)

    def raise_not_contains_in_dict(self, text: str) -> NoReturn:
        raise TranslationNotExistException(text, self.lang_from, self.lang_to)


TranslationDictionary = Dict[str, str]


class PresetDictionaryTranslator(Translator):
    def __init__(
            self,
            dictionary: TranslationDictionary,
            lang_from: Language,
            lang_to: Language
    ):
        super().__init__(lang_from, lang_to)
        self.dictionary: TranslationDictionary = dictionary

    def translate(self, text: str) -> str:
        if text not in self.dictionary:
            self.raise_not_contains_in_dict(text)
        return self.dictionary[text]
