import abc
from typing import Callable, List

OutputStream = Callable[[str], None]


class CommandHandler(abc.ABC):
    @abc.abstractmethod
    def handle_command(self, command: str, out_stream: OutputStream) -> None:
        pass

    @abc.abstractmethod
    def handle_input(self, inp: str, out_stream: OutputStream) -> None:
        pass

    @abc.abstractmethod
    def handle_get_info(self, out_stream: OutputStream) -> None:
        pass

    @abc.abstractmethod
    def get_all_commands(self) -> List[str]:
        pass
