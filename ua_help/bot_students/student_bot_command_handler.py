import enum
from typing import List, Optional, Tuple, Callable

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.bot_students.student_form import student_form
from ua_help.common.command_handler import CommandHandler, OutputStream
from ua_help.form.field.common_fields import field_select_language
from ua_help.form.field.form_field import FormField
from ua_help.form.form import TextForm
from ua_help.localize.language import Language
from ua_help.localize.localize import localizer_to, Localized, InfoMessage


class StudentBotState(enum.Enum):
    IDLE = 0
    LANGUAGE_SELECTION = 1
    FORM_FILL = 2


class StudentBotCommandHandler(CommandHandler):
    def __init__(self, config: StudentTelegramFormConfig, result_consumer: Callable[[List[Tuple[str, str]]], None]):
        self.result_consumer: Callable[[List[Tuple[str, str]]], None] = result_consumer
        self.student_form: Optional[TextForm] = None
        self.chosen_language: Optional[Language] = None
        self.language_field: FormField = field_select_language()
        self.state = StudentBotState.IDLE
        self.config = config
        self.info: Localized = Localized.from_folder(config.intro_folder)
        self.default_language = Language.UA

    def get_all_commands(self) -> List[str]:
        return ['start', 'language']

    def __handle_start_filling(self, out_stream: OutputStream):
        self.state = StudentBotState.FORM_FILL
        self.student_form = student_form(self.config, localizer_to(self.chosen_language))
        self.student_form.print_info_to_stream(out_stream)

    def __handle_start_choosing_language(self, out_stream: OutputStream):
        self.state = StudentBotState.LANGUAGE_SELECTION
        self.language_field.print_info_to_stream(out_stream)
        self.language_field.print_help_to_stream(out_stream)

    def handle_command(self, command: str, out_stream: OutputStream) -> None:
        if command == 'start':
            if self.chosen_language is None:
                self.__handle_start_choosing_language(out_stream)
            else:
                self.__handle_start_filling(out_stream)
        elif command == 'language':
            self.chosen_language = None
            self.__handle_start_choosing_language(out_stream)

    def translate(self, localized: Localized):
        return localized.translate_to(
            self.default_language if self.chosen_language is None else self.chosen_language
        )

    def handle_input(self, inp: str, out_stream: OutputStream) -> None:
        if self.state == StudentBotState.IDLE:
            out_stream(self.translate(InfoMessage.PUT_START_COMMAND.value))
        elif self.state == StudentBotState.LANGUAGE_SELECTION:
            selected = self.language_field.try_read_value(inp, out_stream)
            if selected is not None:
                self.chosen_language = Language.from_str(selected)
                self.language_field = field_select_language()
                self.__handle_start_filling(out_stream)
        elif self.state == StudentBotState.FORM_FILL:
            result = self.student_form.put_user_input(inp, out_stream)
            if result is not None:
                self.result_consumer(result)
                self.student_form = None
                self.state = StudentBotState.IDLE

    def handle_get_info(self, out_stream: OutputStream) -> None:
        out_stream(self.translate(self.info))
