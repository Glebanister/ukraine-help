from ua_help.exception.categorized_exception import ToInformUserExceptionWithInfo
from ua_help.localize.localize import Localized


class FieldInvalidFillException(ToInformUserExceptionWithInfo):
    def __init__(self, info: Localized):
        super().__init__(info)
