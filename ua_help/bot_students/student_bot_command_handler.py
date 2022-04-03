import enum
import datetime
import json
from pathlib import Path
from typing import List, Optional, Tuple, Callable, Dict

from telegram import Chat

from ua_help.bot_students.config import StudentTelegramFormConfig
from ua_help.bot_students.student_form import student_form
from ua_help.common.command_handler import CommandHandler
from ua_help.exception.categorized_exception import ToInformUserWithLocalizedMessage, ToInformUserException
from ua_help.form.field.common_fields import field_select_language
from ua_help.form.field.form_field import FormField, TelegramContext
from ua_help.form.form import TextForm
from ua_help.localize.language import Language
from ua_help.localize.localize import localizer_to, Localized, InfoMessage
from ua_help.telegram.util import send_error, send_plain_text

MAX_FORMS_PER_CLIENT = 5


class JsonState(enum.Enum):
    SENT_FORMS = 'sent_forms'
    FORMS_LIMIT = 'forms_limit'
    LAST_ACTIVITY = 'last_activity_datetime'
    CHOSEN_LANGUAGE = 'chosen_language'


class StudentBotState(enum.Enum):
    IDLE = 0
    LANGUAGE_SELECTION = 1
    FORM_FILL = 2


class StudentBotCommandHandler(CommandHandler):
    def __init__(
            self,
            config: StudentTelegramFormConfig,
            result_consumer: Callable[[List[Tuple[str, str]]], Dict[str, str]],
            chat: Chat
    ):
        self.chat = chat
        self.result_consumer: Callable[[List[Tuple[str, str]]], Dict[str, str]] = result_consumer
        self.student_form: Optional[TextForm] = None
        self.chosen_language: Optional[Language] = None
        self.language_field: Optional[FormField] = None
        self.state = StudentBotState.IDLE
        self.config = config
        self.info: Localized = Localized.from_folder(config.intro_folder)
        self.default_language = config.default_language
        self.sent_forms: List[Dict[str, str]] = []
        self.forms_limit = MAX_FORMS_PER_CLIENT
        self.last_activity_datetime: Optional[datetime.datetime] = None
        self.reboot_state_from_disk()

    def chat_file_path(self) -> Path:
        clients_folder = self.config.clients_data
        clients_folder.mkdir(exist_ok=True)
        this_client_file = (clients_folder / str(self.chat.id)).with_suffix('.json')
        return this_client_file

    def flush_state_to_disk(self):
        state = {
            JsonState.SENT_FORMS.value: self.sent_forms,
            JsonState.FORMS_LIMIT.value: self.forms_limit,
            JsonState.LAST_ACTIVITY.value: str(self.last_activity_datetime.isoformat()),
            JsonState.CHOSEN_LANGUAGE.value: None if self.chosen_language is None else str(self.chosen_language.name)
        }
        with self.chat_file_path().open('w') as chat_file:
            chat_file.write(json.dumps(state))

    def reboot_state_from_disk(self):
        chat_file_path = self.chat_file_path()
        if not self.chat_file_path().exists():
            return

        with chat_file_path.open('r') as chat_file:
            chat_file_content = chat_file.read()
            if chat_file_content.strip() == '':
                return

            state = json.loads(chat_file_content)
            lang_in_state = state[JsonState.CHOSEN_LANGUAGE.value]
            self.sent_forms = state[JsonState.SENT_FORMS.value]
            self.forms_limit = int(state[JsonState.FORMS_LIMIT.value])
            self.last_activity_datetime = datetime.datetime.fromisoformat(state[JsonState.LAST_ACTIVITY.value])
            self.chosen_language = Language.from_str(lang_in_state) if lang_in_state is not None else None

    def get_all_commands(self) -> List[str]:
        return ['start', 'language', 'help']

    def __set_idle(self):
        self.state = StudentBotState.IDLE
        self.student_form = None
        self.language_field = None

    def __handle_continue_filling(self, tg: TelegramContext):
        self.state = StudentBotState.FORM_FILL
        assert self.student_form is not None
        self.student_form.send_actual_field_info(tg)

    def __handle_reload(self, tg: TelegramContext):
        self.reboot_state_from_disk()
        send_plain_text(self.translate(InfoMessage.STATE_UPDATED.value), tg)

    def __handle_start_filling(self, tg: TelegramContext):
        if not self.__may_start_form():
            send_error(self.translate(InfoMessage.FORMS_LIMIT_EXCEEDED.value), tg)
            return
        self.state = StudentBotState.FORM_FILL
        self.student_form = student_form(self.config, localizer_to(self.chosen_language))
        self.student_form.send_info_message(tg)

    def __handle_start_choosing_language(self, tg: TelegramContext):
        self.chosen_language = None
        self.state = StudentBotState.LANGUAGE_SELECTION
        self.language_field = field_select_language()
        self.language_field.send_help(tg)

    def __handle_help(self, tg: TelegramContext):
        send_plain_text(self.translate(Localized.from_folder(self.config.help_folder)), tg)

    def __handle_language_set(self, tg: TelegramContext):
        send_plain_text(self.translate(InfoMessage.LANGUAGE_IS_SET.value), tg)

    def __forms_left(self):
        return self.forms_limit - len(self.sent_forms)

    def __may_start_form(self):
        return self.__forms_left() > 0

    def __suggest_fill_more_forms(self, tg: TelegramContext):
        suggest_text = f'{self.translate(InfoMessage.YOU_MAY_SUBMIT_MORE_FORMS.value)}: {self.__forms_left()}'
        if self.__forms_left() > 0:
            suggest_text += '\n' + self.translate(InfoMessage.INPUT_START_COMMAND_TO_FILL.value)
        send_plain_text(suggest_text, tg)

    def __try_continue_filling_something(self, tg: TelegramContext):
        if self.language_field is not None:
            self.__handle_start_choosing_language(tg)
        elif self.student_form is not None:
            self.__handle_continue_filling(tg)

    def handle_command(self, command: str, tg: TelegramContext) -> None:
        self.last_activity_datetime = datetime.datetime.now()
        try:
            if command == 'start':
                if self.chosen_language is None:
                    self.__handle_start_choosing_language(tg)
                else:
                    self.__handle_start_filling(tg)
            elif command == 'language':
                self.__handle_start_choosing_language(tg)
            elif command == 'help':
                self.__handle_help(tg)
                self.__suggest_fill_more_forms(tg)
                self.__try_continue_filling_something(tg)
            elif command == 'update':
                self.__handle_reload(tg)
            else:
                send_error(self.translate(InfoMessage.COMMAND_NOT_FOUND.value), tg)
                self.__handle_help(tg)
        except ToInformUserException as e:
            send_error(e.localized(self.translate), tg)
        finally:
            self.flush_state_to_disk()

    def translate(self, localized: Localized):
        return localized.translate_to(
            self.default_language if self.chosen_language is None else self.chosen_language
        )

    def handle_input(self, inp: str, tg: TelegramContext) -> None:
        self.last_activity_datetime = datetime.datetime.now()
        try:
            if self.state == StudentBotState.IDLE:
                send_error(self.translate(InfoMessage.PUT_START_COMMAND.value), tg)

            elif self.state == StudentBotState.LANGUAGE_SELECTION:
                selected = self.language_field.try_read_value(inp, tg)
                if selected is not None:
                    self.chosen_language = Language.from_str(selected)
                    self.language_field = None
                    if self.student_form is not None:
                        self.student_form.set_localize(localizer_to(self.chosen_language))
                        self.__handle_continue_filling(tg)
                    elif not self.sent_forms:
                        self.__handle_start_filling(tg)
                    else:
                        self.__handle_language_set(tg)
                        self.__suggest_fill_more_forms(tg)

            elif self.state == StudentBotState.FORM_FILL:
                result = self.student_form.put_user_input(inp, tg)
                if result is not None:
                    self.sent_forms.append(self.result_consumer(result))
                    self.__suggest_fill_more_forms(tg)
                    self.__set_idle()
        except ToInformUserException as e:
            send_error(e.localized(self.translate), tg)
        finally:
            self.flush_state_to_disk()

    def handle_get_info(self, tg: TelegramContext) -> None:
        send_plain_text(self.translate(self.info), tg)
