from typing import Any

class Node:
    name: str = ""
    description: str = ""
    color: list[float] = [0.5, 0.5, 0.5, 1]
    CInformation: str = ""
    Id: int = 0

    def __init__(self, inputs: list[str], outputs: list[str], params: list[str] = []) -> None:
        self.name = self.name
        self.description = self.description
        self.color = self.color
        self.CInformation = self.CInformation
        self.Id = id(self)
        self.inputs: dict[str, Any] = {inp: None for inp in inputs}
        self.outputs: dict[str, Any] = {out: None for out in outputs}
        self.params: dict[str, str | None] = {param: None for param in params}
    
    def onValidate(self) -> None:
        pass

    def setParam(self, paramName: str, paramValue: str) -> Any:
        self.params[paramName] = paramValue
        return self

    def eval(self) -> None:
        for x in self.outputs:
            self.outputs[x] = None
        return

    def code(self) -> str:
        return ""


class ValueType(Node):
    name = "Value Node"
    description = "The node designed to resolve values links."

    def __init__(self) -> None:
        super().__init__([], ["Value"], ["Value"])
        
    def eval(self) -> None:
        self.outputs["Value"] = self.params["Value"]
        return 
    
    def code(self) -> str:
        return str(self.params["Value"])


class NodePoint:
    parent: Node
    valueName: str

    def __init__(self, parent: Node, valueName: str) -> None:
        self.parent = parent
        self.valueName = valueName

    def eval(self) -> ValueType:
        self.parent.eval()
        return ValueType().setParam("Value", self.parent.outputs[self.valueName])
    
    def code(self) -> str:
        return self.parent.code()