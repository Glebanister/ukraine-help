import abc
from typing import Callable, List

from ua_help.telegram.util import TelegramContext

OutputStream = Callable[[str], None]


class CommandHandler(abc.ABC):
    @abc.abstractmethod
    def handle_command(self, command: str, tg: TelegramContext) -> None:
        pass

    @abc.abstractmethod
    def handle_input(self, inp: str, tg: TelegramContext) -> None:
        pass

    @abc.abstractmethod
    def handle_get_info(self, tg: TelegramContext) -> None:
        pass

    @abc.abstractmethod
    def get_all_commands(self) -> List[str]:
        pass
