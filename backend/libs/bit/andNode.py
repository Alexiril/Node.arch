import backend.core.node as node

class andNode(node.Node):
    
    def __init__(self) -> None:
        super().__init__(2, 1)

    def eval(self) -> None:
        self.outputs[0] = node.ValueType(self.inputs[0].eval() & self.inputs[1].eval())
        return
    
    def code(self) -> str:
        return f"({self.inputs[0].code()} && {self.inputs[1].code()})"