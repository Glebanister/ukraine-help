import re
from typing import Callable

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.form.field.info_field import InfoField
from ua_help.form.field.multiple_variants_field import MultipleVariantsField
from ua_help.form.field.radio_button_field import RadioButtonField
from ua_help.form.field.text_field import TextField
from ua_help.form.form import TextForm
from ua_help.localize.localize import Localized, InfoMessage


def student_form(config: StudentTelegramFormConfig, localize: Callable[[Localized], str]) -> TextForm:
    form = TextForm(
        Localized(
            'Collecting applications for educational assistance',
            'Збір заявок на освітню допомогу',
            'Сбор заявок на образовательную помощь'
        ),
        InfoMessage.FINISH_STUDENT_INPUT.value,
        localize
    )

    form.add_field(InfoField(
        label=Localized(
            'Volunteer project "Educational bridge"',
            'Волонтерський проект "Освітня допомога"',
            'Волонтёрский проект "Образовательный мост"'
        ),
        information=Localized.from_folder(config.intro_folder)
    ))

    form.add_field(RadioButtonField(
        'role',
        Localized('Who are you?', 'Хто ви?', 'Кто вы?'),
        [
            (Localized('Parent (guardian)', 'Батько (опікун)', 'Родитель (опекун)'), 'parent'),
            (Localized('Student', 'Учень', 'Ученик'), 'student'),
        ],
        is_required=True,
    ))

    form.add_field(TextField(
        'name',
        Localized('Student\'s name', 'Ім\'я учня', 'Имя ученика'),
        re.compile(r'.*'),
        Localized(
            'First and last name in any language',
            'Ім\'я та прізвище будь-якою мовою',
            'Имя и фамилия на любом языке'
        ),
        is_required=True
    ))

    form.add_field(RadioButtonField(
        'grade',
        Localized('Grade', 'Клас', 'Класс'),
        Localized.integers(range(1, 13), Localized('grade', 'клас', 'класс')),
        is_required=True,
    ))

    form.add_field(RadioButtonField(
        'graduation_this_year',
        Localized(
            'Graduation planned for this year',
            'Випускний планується цього року',
            'Выпуск планировался в этом году'
        ),
        Localized.yes_no(),
        is_required=True,
    ))

    form.add_field(MultipleVariantsField(
        key='speaking_languages',
        label=Localized(
            '''Languages in which they are willing to learn.
If there is an additional language, select the "Other" option and you will have the opportunity to specify it at the end of the form
            ''',
            '''Мови, на яких готові навчатися.
Якщо є додаткова мова, щоб вибрати варіант "Другой" і у вас буде у формі його вказівки
            ''',
            '''Языки, на которых готовы обучаться.
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

    form.add_field(InfoField(
        label=Localized(
            'Selecting Priority Subjects',
            'Вибір пріоритетних предметів',
            'Выбор приоритетных предметов'
        ),
        information=Localized.from_folder(config.priority_choice)
    ))

    form.add_field(RadioButtonField(
        key='subject_1_priority',
        label=Localized(
            'Subject of the first priority',
            'Предмет першого пріоритету',
            'Предмет первого приоритета'
        ),

        choices=Localized.choices_from_json(config.subjects_file),
        is_required=True,
    ))

    form.add_field(RadioButtonField(
        key='subject_2_priority',
        label=Localized(
            'Subject of the second priority',
            'Предмет другого пріоритету',
            'Предмет второго приоритета'
        ),
        choices=Localized.choices_from_json(config.subjects_file),
        is_required=False,
    ))

    form.add_field(RadioButtonField(
        key='subject_3_priority',
        label=Localized(
            'Subject of the first priority',
            'Предмет третього пріоритету',
            'Предмет третьего приоритета'
        ),

        choices=Localized.choices_from_json(config.subjects_file),
        is_required=False,
    ))

    form.add_field(InfoField(
        label=Localized(
            'If you have chosen any of the languages',
            'Якщо ви обрали будь-яку іноземну мову',
            'Если вы выбрали какой-либо из иностранных языков'
        ),
        information=Localized.from_folder(config.languages_notice)
    ))

    form.add_field(RadioButtonField(
        'ready_work_with_russian_teacher',
        Localized(
            'Ready to work with russian teacher',
            'Готові займатися з викладачем з Росії ',
            'Готовы заниматься с преподавателем из России'
        ),
        Localized.yes_no(),
        is_required=True,
    ))

    form.add_field(RadioButtonField(
        key='upcoming_exam',
        label=Localized(
            'What exams are you planning to take this year?',
            'Які іспити планували складати цього року?',
            'Какие экзамены планировали сдавать в этом году?'
        ),

        choices=[
            (
                Localized('ВНО (ЗНО)', 'ВНО (ЗНО)', 'ВНО (ЗНО)'),
                'vno'
            ),
            (
                Localized('ЕГЭ', 'ЕГЭ', 'ЕГЭ'),
                'ege'
            ),
            (
                Localized('Didn\'t plan', 'Не планували', 'Не планировали'),
                'no'
            ),
        ],
        is_required=True,
    ))

    form.add_field(MultipleVariantsField(
        key='help_format',
        label=Localized(
            'What format of help will suit you?',
            'Який формат допомоги вас влаштовуватиме?',
            'Какой формат помощи вас будет устраивать?'
        ),
        choices=[
            (
                Localized(
                    'Online consultations',
                    'Онлайн - консультації',
                    'Онлайн - консультации'
                ),
                'online_consultations'
            ),
            (
                Localized(
                    'Individual lessons',
                    'Індивідуальне заняття',
                    'Индивидуальные занятия'
                ),
                'individual_lessons'
            ),
            (
                Localized(
                    'Online lessons for a large number of students',
                    'Онлайн-уроки на велику кількість слухачів',
                    'Онлайн-уроки на большое количество слушателей'
                ),
                'online_lessons_large_class'
            ),
            (
                Localized(
                    'Answering questions in social networks or messenger',
                    'Відповіді на запитання у соцмережах чи месенджері',
                    'Ответы на вопросы в соцсетях или мессенджере'
                ),
                'social_networks'
            ),
            (
                Localized(
                    'Online answers to questions in social networks or messenger',
                    'Допомога у складанні індивідуального плану навчання з обраного предмета',
                    'Помощь в составлении индивидуального плана обучения по выбранному предмету'
                ),
                'individual_plan'
            ),
            (
                Localized(
                    'Selecting materials from open sourcesr',
                    'Підбір матеріалів із відкритих джерел',
                    'Подбор материалов из открытых источников'
                ),
                'open_source_materials'
            ),
        ],
        default_choice=None,
        bound_min=1,
        bound_max=None,
    ))

    form.add_field(InfoField(
        label=Localized(
            'Selecting Priority Subjects',
            'Вибір пріоритетних предметів',
            'Выбор приоритетных предметов'
        ),
        information=Localized.from_folder(config.priority_choice)
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

    form.add_field(TextField(
        'comments',
        Localized(
            'Other comments',
            'Коментарі до форми',
            'Комментарии к форме'
        ),
        re.compile(r'.?'),
        Localized(
            'Any comment with one message',
            'Будь-який коментар одним повідомленням',
            'Любой комментарий одним сообщением'
        ),
        is_required=False
    ))

    form.add_field(TextField(
        'other_communications',
        Localized(
            'Other ways to quickly communicate with you (pages in social networks, your login in Telegram, etc.)',
            'Інші способи швидкої комунікації з вами (сторінки в соцмережах, ваш логін у Telegram тощо)',
            'Другие способы быстрой коммуникации с вами (страницы в соцсетях, ваш логин в Telegram и т.д.)'
        ),
        re.compile(r'.?'),
        Localized(
            'Links to you in https:// format in one message',
            'Посилання на вас у форматі https:// одним повідомленням',
            'Ссылки на вас в формате https:// одним сообщением'
        ),
        is_required=False
    ))

    return form
