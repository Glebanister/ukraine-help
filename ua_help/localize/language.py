import enum


class Language(enum.Enum):
    EN = 'English'
    UA = 'Українська'
    RU = 'Русский'

    def __repr__(self):
        return self.value

    @classmethod
    def from_str(cls, language_repr):
        patterns = {
            Language.EN: ['en', 'english', 'eng', 'английский', 'англійська', 'англ'],
            Language.UA: ['українська', 'украинский'],
            Language.RU: ['русский', 'рус', 'ру']
        }
        for lang, patt in patterns.items():
            if language_repr.lower() in patt:
                return lang
        raise Exception(f'Language {language_repr} is not defined')
