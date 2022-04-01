import enum

from typing import Optional, Callable

from ua_help.localize.localize import Localized


class ErrorCategory(enum.Enum):
    TO_INFORM_USER = 0
    TO_FAIL = 1


class CategorizedException(Exception):
    def __init__(
            self,
            category: ErrorCategory,
            actor: Optional[str],
            local: Optional[Localized],
            non_local: Optional[str]
    ):
        self.category = category
        self.actor = actor
        self.local = local
        self.non_local = non_local

    def __repr__(self) -> str:
        actor = '' if self.actor is None else f'{self.actor}: '
        return f'{actor}{self.local} {self.non_local}'

    def localized(self, localize: Callable[[Localized], str]) -> str:
        if self.local is not None:
            return localize(self.local)
        elif self.non_local is not None:
            return self.non_local
        return ''


class ToInformUserException(CategorizedException):
    def __init__(self, info: Optional[Localized], msg: Optional[str]):
        super().__init__(ErrorCategory.TO_INFORM_USER, None, info, msg)


class ToInformUserExceptionWithInfo(ToInformUserException):
    def __init__(self, info: Localized):
        super().__init__(info, None)


class ToInformUserWithLocalizedMessage(ToInformUserException):
    def __init__(self, info: str):
        super().__init__(None, info)


class ToFailException(CategorizedException):
    def __init__(self, actor: Optional[str], message: str):
        super().__init__(ErrorCategory.TO_FAIL, actor, None, message)
