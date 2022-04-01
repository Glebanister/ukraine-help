from ua_help.form.form import TextForm
from ua_help.localize.localize import Localized


def read_string() -> str:
    return input()


def print_string(s: str) -> None:
    print(s)


def main():
    form = TextForm(Localized('Some form', 'Текст на украинском', 'Форма'), read_string, print_string)
    form.read_fields()


if __name__ == '__main__':
    main()
