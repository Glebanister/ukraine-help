import enum


class Language(enum.Enum):
    EN = 'English'
    UA = 'Українська'
    RU = 'Русский'

    def __repr__(self):
        return self.value

    @classmethod
    def from_str(cls, language_repr: str):
        patterns = {
            Language.EN: ['language.en', 'en', 'english', 'eng', 'английский', 'англійська', 'англ'],
            Language.UA: ['language.ua', 'ua', 'українська', 'украинский'],
            Language.RU: ['language.ru', 'ru', 'русский', 'рус', 'ру']
        }
        for lang, patterns in patterns.items():
            for pattern in patterns:
                if language_repr.lower() == pattern.lower():
                    return lang
        raise Exception(f'Language {language_repr} is not defined')
