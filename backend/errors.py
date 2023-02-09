import sys


class CommonError(Exception):

    def __init__(self, *args: object) -> None:
        print(args, file=sys.stderr)
        super().__init__(*args)


class SettingsError(CommonError):
    ...


class LibError(CommonError):
    ...


class ThemeError(CommonError):
    ...


class FrontendError(CommonError):
    ...
