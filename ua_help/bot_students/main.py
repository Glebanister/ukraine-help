import re
from pathlib import Path

from ua_help.form.field.multiple_variants_field import MultipleVariantsField
from ua_help.form.field.radio_button_field import RadioButtonField
from ua_help.form.field.text_field import TextField
from ua_help.form.form import TextForm
from ua_help.io.console_io import ConsoleIO
from ua_help.localize.localize import Localized

ROOT = Path('.')
RESOURCES = ROOT / 'resources'

INTRO_FOLDER = RESOURCES / 'intro'
SUBJECTS_FILE = RESOURCES / 'subjects.json'


def main():
    io = ConsoleIO()

    form = TextForm(
        Localized.from_folder(INTRO_FOLDER),
        *io.to_read_write_streams()
    )

    form.add_field(RadioButtonField(
        'role',
        Localized('Who are you?', 'Хто ви?', 'Кто вы?'),
        [
            (Localized('Parent (guardian)', 'Батько (опікун)', 'Родитель (опекун)'), ' parent'),
            (Localized('Student', 'Учень', 'Ученик'), 'student'),
        ]
    ))

    form.add_field(TextField(
        'name',
        Localized('Student\'s name', 'Ім\'я учня', 'Имя ученика'),
        re.compile(r'.*'),
        Localized('Name in any language', 'Ім\'я будь-якою мовою', 'Имя на любом языке'),
        is_required=True
    ))

    form.add_field(RadioButtonField(
        'grade',
        Localized('Grade', 'Клас', 'Класс'),
        Localized.integers(range(1, 13), Localized(' grade', 'клас', ' класс'))
    ))

    form.add_field(RadioButtonField(
        'graduation_this_year',
        Localized(
            'Graduation planned for this year',
            'Випускний планується цього року',
            'Выпуск планировался в этом году'
        ),
        Localized.yes_no()
    ))

    form.add_field(MultipleVariantsField(
        key='speaking_languages',
        label=Localized(
            '''
Languages in which they are willing to learn.
If there is an additional language, select the "Other" option and you will have the opportunity to specify it at the end of the form
            ''',
            '''
Мови, на яких готові навчатися.
Якщо є додаткова мова, щоб вибрати варіант "Другой" і у вас буде у формі його вказівки
            ''',
            '''
Языки, на которых готовы обучаться.
Если есть дополнительный язык, то выберите вариант 'Другой язык' и у вас будет в конце формы возможность его указать
            '''
        ),
        choices=[
            (
                Localized('Ukrainian language', 'Українська мова', 'Украинский язык'),
                'ukrainian'
            ),
            (
                Localized('Russian language', 'Російська мова', 'Русский язык'),
                'russian'
            ),
            (
                Localized('English language', 'Українська мова', 'Английский язык'),
                'english'
            ),
            (
                Localized('Other language', 'Інша мова (вкажіть у коментарі)', 'Другой язык (укажите в комментарии)'),
                'other'
            ),
        ],
        default_choice=None,
        bound_min=1,
        bound_max=None,
    ))

    form.add_field(RadioButtonField(
        key='subject_first_priority',
        label=Localized(
            '''
Choice of priority subjects
You will be asked to choose four priority subjects, among which you will also need to choose the highest priority subject.
            ''',
            '''
Вибір пріоритетних предметів
Виберіть найпріоритетніший предмет. серед яких вам також потрібно буде обрати найпріоритетніший предмет.
            ''',
            '''
Выбор приоритетного предмета
Выберите самый приоритетный для вас предмет. По ньому ми шукатимемо для вас викладача насамперед.
            '''
        ),

        choices=Localized.choices_from_json(SUBJECTS_FILE)
    ))

    form.add_field(TextField(
        'email',
        Localized(
            'Contact email address',
            'Адреса електронної пошти',
            'Адрес электронной почты для связи'
        ),
        re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
        Localized('example@example.com', 'example@example.com', 'example@example.com'),
        is_required=True
    ))

    form.add_field(RadioButtonField(
        'ready_work_with_russian',
        Localized(
            'Ready to work with russian teacher',
            'Готові займатися з викладачем з Росії ',
            'Готовы заниматься с преподавателем из России'
        ),
        Localized.yes_no()
    ))

    print(form.read_fields())


if __name__ == '__main__':
    main()
