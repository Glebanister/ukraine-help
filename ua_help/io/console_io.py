from ua_help.io.io import IO


class ConsoleIO(IO):
    def read_string(self) -> str:
        return input()

    def print_string(self, s: str) -> None:
        print(s)
