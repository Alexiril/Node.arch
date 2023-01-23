from typing import Any

class ValueType:
    value: bool

    def __init__(self, value: bool = False) -> None:
        self.value = value

    def eval(self) -> None:
        return self.value
    
    def code(self) -> str:
        return "true" if self.value else "false"

class Node:

    def __init__(self, inputs: int = 0, outputs: int = 0) -> None:
        self.name: str = ""
        self.inputs: list[None | ValueType] = [None for i in range(inputs)]
        self.outputs: list[None | ValueType] = [None for i in range(outputs)]
        self.params: dict[str, Any] = dict()

    def eval(self) -> None:
        self.outputs = self.inputs
        return

    def code(self) -> str:
        return ""