import sys

class SettingsError(Exception):

    def __init__(self, *args: object) -> None:
        print(args, file=sys.stderr)
        super().__init__(*args)

class LibError(Exception):
    
    def __init__(self, *args: object) -> None:
        print(args, file=sys.stderr)
        super().__init__(*args)

class ThemeError(Exception):

    def __init__(self, *args: object) -> None:
        print(args, file=sys.stderr)
        super().__init__(*args)