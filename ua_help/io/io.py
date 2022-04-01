import abc
from typing import Tuple, Callable


class IO(abc.ABC):
    @abc.abstractmethod
    def read_string(self) -> str:
        pass

    @abc.abstractmethod
    def print_string(self, s: str) -> None:
        pass

    def to_read_write_streams(self) -> Tuple[Callable[[], str], Callable[[str], None]]:
        return (
            self.read_string,
            self.print_string
        )
