class InputValidationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args[0]


class ApplicationValidationError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        self.message = args[0]
